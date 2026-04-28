# bq_explorer.py
# Drop this file into any Vertex Workbench notebook and run:
#   %run bq_explorer.py          — launches with no args, UI guides you
#   from bq_explorer import explore; explore()   — same effect
#   explore(project_id="my-project")             — skip project input
#   explore(project_id="my-project", dataset_id="my_dataset")  — jump to tables
#
# To pull from GCS:
#   !gsutil cp gs://YOUR_BUCKET/bq_explorer.py .
#   %run bq_explorer.py

# === IMPORTS ===

from __future__ import annotations

from typing import Optional

import pandas as pd
import ipywidgets as widgets
from IPython.display import display as ipy_display, HTML
from google.cloud import bigquery

# === BQ CLIENT ===


def _get_client(project_id: str) -> bigquery.Client:
    return bigquery.Client(project=project_id)


def list_datasets(client: bigquery.Client, project_id: str) -> list[str]:
    datasets = client.list_datasets(project=project_id)
    return sorted(ds.dataset_id for ds in datasets)


def list_tables(
    client: bigquery.Client, project_id: str, dataset_id: str
) -> list[str]:
    tables = client.list_tables(f"{project_id}.{dataset_id}")
    return sorted(t.table_id for t in tables)


def preview_table(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    table_id: str,
    limit: int,
) -> pd.DataFrame:
    query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}` LIMIT @row_limit"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("row_limit", "INT64", limit)
        ]
    )
    return client.query(query, job_config=job_config).to_dataframe()


def get_table_metadata(
    client: bigquery.Client,
    project_id: str,
    dataset_id: str,
    table_id: str,
) -> dict:
    table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")
    return {
        "num_rows": table.num_rows,
        "num_bytes": table.num_bytes,
        "description": table.description or "",
        "schema": table.schema,
    }


# === WIDGETS ===


class BQExplorer:
    """Self-contained BigQuery browser widget for Jupyter / Vertex AI Workbench."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        dataset_id: Optional[str] = None,
        default_rows: int = 20,
    ) -> None:
        # dataset_id is only meaningful when project_id is also given
        if dataset_id is not None and project_id is None:
            dataset_id = None

        # --- State ---
        self._project_id: Optional[str] = project_id
        self._dataset_id: Optional[str] = dataset_id
        self._default_rows: int = default_rows

        self._client: Optional[bigquery.Client] = None
        self._table_id: Optional[str] = None
        self._df_full: Optional[pd.DataFrame] = None
        self._metadata: Optional[dict] = None
        self._checkboxes: dict[str, widgets.Checkbox] = {}

        # --- Build widgets (no I/O) ---
        self._build_panel0()
        self._build_panel1()
        self._build_panel2()
        self._build_panel3()

        # --- Assemble main container ---
        self.main_vbox = widgets.VBox([
            self._panel0_box,
            self._panel1_box,
            self._panel2_box,
            self._panel3_box,
        ])

        # --- Initial visibility ---
        self._apply_initial_visibility()

        # --- Eager data load when args were supplied ---
        if project_id is not None:
            try:
                self._client = _get_client(project_id)
            except Exception as exc:
                self._show(self._panel0_box)
                with self._conn_out:
                    ipy_display(HTML(
                        f"<span style='color:red'>Client init failed: {exc}</span>"
                    ))
                return

            if dataset_id is not None:
                self._load_tables(dataset_id)
            else:
                self._load_datasets()

    # ------------------------------------------------------------------
    # Panel builders — create widgets and wire observers, never do I/O
    # ------------------------------------------------------------------

    def _build_panel0(self) -> None:
        self._conn_project = widgets.Text(
            description="Project ID:",
            placeholder="my-gcp-project",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="400px"),
        )
        self._conn_dataset = widgets.Text(
            description="Dataset ID (optional):",
            placeholder="my_dataset",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="400px"),
        )
        self._conn_btn = widgets.Button(
            description="Connect",
            button_style="primary",
        )
        self._conn_out = widgets.Output()
        self._conn_btn.on_click(self._on_connect)
        self._panel0_box = widgets.VBox([
            widgets.HTML("<h3 style='margin:4px 0'>BigQuery Explorer</h3>"),
            self._conn_project,
            self._conn_dataset,
            self._conn_btn,
            self._conn_out,
        ])

    def _build_panel1(self) -> None:
        self._dataset_select = widgets.Select(
            options=[],
            description="Dataset:",
            rows=15,
            style={"description_width": "initial"},
            layout=widgets.Layout(width="400px"),
        )
        self._panel1_out = widgets.Output()
        self._dataset_select.observe(self._on_dataset_select, names="value")
        self._panel1_box = widgets.VBox([
            widgets.HTML("<h3 style='margin:4px 0'>Datasets</h3>"),
            self._dataset_select,
            self._panel1_out,
        ])

    def _build_panel2(self) -> None:
        self._table_select = widgets.Select(
            options=[],
            description="Table:",
            rows=15,
            style={"description_width": "initial"},
            layout=widgets.Layout(width="400px"),
        )
        self._panel2_out = widgets.Output()
        self._table_select.observe(self._on_table_select, names="value")
        self._panel2_box = widgets.VBox([
            widgets.HTML("<h3 style='margin:4px 0'>Tables</h3>"),
            self._table_select,
            self._panel2_out,
        ])

    def _build_panel3(self) -> None:
        self._rows_slider = widgets.IntSlider(
            value=self._default_rows,
            min=10,
            max=500,
            step=10,
            description="Rows to preview:",
            continuous_update=False,
            style={"description_width": "initial"},
            layout=widgets.Layout(width="500px"),
        )
        self._rows_slider.observe(self._on_rows_change, names="value")

        self._col_filter = widgets.Text(
            description="Filter columns:",
            placeholder="type to narrow…",
            style={"description_width": "initial"},
            layout=widgets.Layout(width="400px"),
        )
        self._col_filter.observe(self._on_col_filter_change, names="value")

        self._checkbox_vbox = widgets.VBox(
            [],
            layout=widgets.Layout(
                max_height="200px",
                overflow_y="auto",
                border="1px solid #ccc",
                padding="4px",
            ),
        )

        self._preview_out = widgets.Output()
        self._schema_out = widgets.Output()
        self._meta_out = widgets.Output()

        self._panel3_box = widgets.VBox([
            widgets.HTML("<h3 style='margin:4px 0'>Data Viewer</h3>"),
            self._rows_slider,
            self._meta_out,
            self._preview_out,
            widgets.HTML("<h4 style='margin:8px 0 4px'>Schema</h4>"),
            self._schema_out,
            widgets.HTML("<h4 style='margin:8px 0 4px'>Column Filter</h4>"),
            self._col_filter,
            self._checkbox_vbox,
        ])

    # ------------------------------------------------------------------
    # Visibility helpers
    # ------------------------------------------------------------------

    def _show(self, box: widgets.VBox) -> None:
        box.layout.display = ""

    def _hide(self, box: widgets.VBox) -> None:
        box.layout.display = "none"

    def _apply_initial_visibility(self) -> None:
        self._hide(self._panel0_box)
        self._hide(self._panel1_box)
        self._hide(self._panel2_box)
        self._hide(self._panel3_box)

        if self._project_id is None:
            self._show(self._panel0_box)
        elif self._dataset_id is None:
            self._show(self._panel1_box)
        else:
            self._show(self._panel2_box)

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _on_connect(self, _btn_event) -> None:
        self._conn_out.clear_output()
        project = self._conn_project.value.strip()
        dataset = self._conn_dataset.value.strip()

        if not project:
            with self._conn_out:
                ipy_display(HTML(
                    "<span style='color:red'>Project ID is required.</span>"
                ))
            return

        try:
            self._client = _get_client(project)
            self._project_id = project
        except Exception as exc:
            with self._conn_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Client init failed: {exc}</span>"
                ))
            return

        self._hide(self._panel0_box)

        if dataset:
            self._dataset_id = dataset
            self._load_tables(dataset)
        else:
            self._load_datasets()

    def _load_datasets(self) -> None:
        self._panel1_out.clear_output()
        try:
            names = list_datasets(self._client, self._project_id)
        except Exception as exc:
            self._show(self._panel1_box)
            with self._panel1_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Error loading datasets: {exc}</span>"
                ))
            return

        self._show(self._panel1_box)

        if not names:
            with self._panel1_out:
                ipy_display(HTML("<em>No datasets found in this project.</em>"))
            return

        self._dataset_select.unobserve(self._on_dataset_select, names="value")
        self._dataset_select.options = names
        self._dataset_select.value = None
        self._dataset_select.observe(self._on_dataset_select, names="value")

    def _on_dataset_select(self, change) -> None:
        dataset_id = change["new"]
        if dataset_id is None:
            return
        self._dataset_id = dataset_id
        self._load_tables(dataset_id)

    def _load_tables(self, dataset_id: str) -> None:
        self._panel2_out.clear_output()
        try:
            names = list_tables(self._client, self._project_id, dataset_id)
        except Exception as exc:
            self._show(self._panel2_box)
            with self._panel2_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Error loading tables: {exc}</span>"
                ))
            return

        self._show(self._panel2_box)

        if not names:
            with self._panel2_out:
                ipy_display(HTML("<em>No tables found in this dataset.</em>"))
            return

        self._table_select.unobserve(self._on_table_select, names="value")
        self._table_select.options = names
        self._table_select.value = None
        self._table_select.observe(self._on_table_select, names="value")

    def _on_table_select(self, change) -> None:
        table_id = change["new"]
        if table_id is None:
            return
        self._table_id = table_id
        self._load_table_data(table_id)

    def _load_table_data(self, table_id: str) -> None:
        self._preview_out.clear_output()
        self._schema_out.clear_output()
        self._meta_out.clear_output()

        try:
            self._metadata = get_table_metadata(
                self._client, self._project_id, self._dataset_id, table_id
            )
        except Exception as exc:
            self._show(self._panel3_box)
            with self._preview_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Metadata error: {exc}</span>"
                ))
            return

        try:
            self._df_full = preview_table(
                self._client,
                self._project_id,
                self._dataset_id,
                table_id,
                self._rows_slider.value,
            )
        except Exception as exc:
            self._show(self._panel3_box)
            with self._preview_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Preview error: {exc}</span>"
                ))
            return

        self._build_checkboxes(list(self._df_full.columns))
        self._render_schema()
        self._render_meta()
        self._update_preview()
        self._show(self._panel3_box)

    def _on_rows_change(self, change) -> None:
        if self._table_id is None:
            return
        previously_unchecked = {
            col for col, cb in self._checkboxes.items() if not cb.value
        }
        try:
            self._df_full = preview_table(
                self._client,
                self._project_id,
                self._dataset_id,
                self._table_id,
                change["new"],
            )
        except Exception as exc:
            with self._preview_out:
                ipy_display(HTML(
                    f"<span style='color:red'>Reload error: {exc}</span>"
                ))
            return

        self._build_checkboxes(list(self._df_full.columns), unchecked=previously_unchecked)
        self._update_preview()

    def _build_checkboxes(
        self,
        columns: list[str],
        unchecked: set[str] | None = None,
    ) -> None:
        if unchecked is None:
            unchecked = set()

        for cb in self._checkboxes.values():
            cb.unobserve_all()

        self._checkboxes = {}
        for col in columns:
            cb = widgets.Checkbox(
                value=(col not in unchecked),
                description=col,
                indent=False,
                layout=widgets.Layout(width="auto"),
            )
            cb.observe(self._on_checkbox_change, names="value")
            self._checkboxes[col] = cb

        filter_text = self._col_filter.value.strip().lower()
        for col, cb in self._checkboxes.items():
            cb.layout.display = "" if filter_text in col.lower() else "none"

        self._checkbox_vbox.children = list(self._checkboxes.values())

    def _on_col_filter_change(self, change) -> None:
        filter_text = change["new"].strip().lower()
        for col, cb in self._checkboxes.items():
            cb.layout.display = "" if filter_text in col.lower() else "none"
        self._update_preview()

    def _on_checkbox_change(self, _change) -> None:
        self._update_preview()

    def _update_preview(self) -> None:
        if self._df_full is None:
            return
        checked_cols = [
            col for col, cb in self._checkboxes.items()
            if cb.value and col in self._df_full.columns
        ]
        self._preview_out.clear_output(wait=True)
        with self._preview_out:
            if not checked_cols:
                ipy_display(HTML("<em>No columns selected.</em>"))
            else:
                ipy_display(self._df_full[checked_cols])

    def _render_schema(self) -> None:
        if self._metadata is None:
            return
        schema_df = pd.DataFrame([
            {"name": f.name, "type": f.field_type, "mode": f.mode}
            for f in self._metadata["schema"]
        ])
        with self._schema_out:
            ipy_display(schema_df)

    def _render_meta(self) -> None:
        if self._metadata is None:
            return
        num_rows = self._metadata["num_rows"]
        num_bytes = self._metadata["num_bytes"] or 0
        size_mb = round(num_bytes / (1024 ** 2), 2)
        desc = self._metadata["description"] or "(no description)"
        html = (
            f"<b>Total rows:</b> {num_rows:,} &nbsp;|&nbsp; "
            f"<b>Size:</b> {size_mb} MB &nbsp;|&nbsp; "
            f"<b>Description:</b> {desc}"
        )
        with self._meta_out:
            ipy_display(HTML(html))

    def display(self) -> None:
        ipy_display(self.main_vbox)


# === ENTRYPOINT ===


def explore(
    project_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    default_rows: int = 20,
) -> BQExplorer:
    """Launch the BigQuery Explorer widget.

    Args:
        project_id:   GCP project. If None, a connection form is shown.
        dataset_id:   Dataset to pre-select. Requires project_id.
        default_rows: Initial row count for the preview slider (10–500).

    Returns:
        The BQExplorer instance.

    Examples::

        explore()                                          # fully guided
        explore(project_id="my-project")                  # skip project input
        explore(project_id="my-project", dataset_id="ds") # jump to tables
    """
    explorer = BQExplorer(
        project_id=project_id,
        dataset_id=dataset_id,
        default_rows=default_rows,
    )
    explorer.display()
    return explorer


if __name__ == "__main__":
    explore()
