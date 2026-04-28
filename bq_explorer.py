# bq_explorer.py
# Drop this file into any Vertex Workbench notebook and run:
#   %run bq_explorer.py          - launches with no args, UI guides you
#   from bq_explorer import explore; explore()   - same effect
#   explore(project_id="my-project")             - skip project input
#   explore(project_id="my-project", dataset_id="my_dataset")  - jump to tables
#
# To pull from GCS:
#   !gsutil cp gs://YOUR_BUCKET/bq_explorer.py .
#   %run bq_explorer.py

import re
import traceback
from typing import Optional

import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output


# === BQ CLIENT =====================================================
# All BigQuery interaction lives here. The google-cloud-bigquery import
# is deferred into get_client() so importing this module on a machine
# without the package installed still works (the error surfaces in the
# widget Output instead of crashing %run).

_IDENT_RE = re.compile(r"^[A-Za-z0-9_\-]+$")


def _check_identifier(name: str, kind: str) -> None:
    if not isinstance(name, str) or not _IDENT_RE.match(name):
        raise ValueError(f"Invalid {kind} identifier: {name!r}")


def get_client(project_id: str):
    """Build a BigQuery client using Application Default Credentials."""
    _check_identifier(project_id, "project")
    try:
        from google.cloud import bigquery
    except ImportError as e:
        raise RuntimeError(
            "google-cloud-bigquery is not installed. On Vertex AI Workbench "
            "this should be preinstalled; elsewhere run: "
            "pip install 'google-cloud-bigquery[pandas]'"
        ) from e
    try:
        return bigquery.Client(project=project_id)
    except Exception as e:
        raise RuntimeError(
            f"Could not initialise BigQuery client for project '{project_id}'. "
            "Check that Application Default Credentials are available "
            "(Vertex Workbench provides these automatically; elsewhere run "
            "`gcloud auth application-default login`). Original error: " + str(e)
        ) from e


def list_datasets(client, project_id: str):
    _check_identifier(project_id, "project")
    return sorted(ds.dataset_id for ds in client.list_datasets(project=project_id))


def list_tables(client, project_id: str, dataset_id: str):
    _check_identifier(project_id, "project")
    _check_identifier(dataset_id, "dataset")
    return sorted(t.table_id for t in client.list_tables(f"{project_id}.{dataset_id}"))


def preview_table(client, project_id: str, dataset_id: str, table_id: str, limit: int) -> pd.DataFrame:
    _check_identifier(project_id, "project")
    _check_identifier(dataset_id, "dataset")
    _check_identifier(table_id, "table")
    n = max(10, min(500, int(limit)))
    sql = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}` LIMIT {n}"
    return client.query(sql).to_dataframe()


def get_table_metadata(client, project_id: str, dataset_id: str, table_id: str) -> dict:
    _check_identifier(project_id, "project")
    _check_identifier(dataset_id, "dataset")
    _check_identifier(table_id, "table")
    table = client.get_table(f"{project_id}.{dataset_id}.{table_id}")
    schema = [(f.name, f.field_type, f.mode or "NULLABLE") for f in table.schema]
    return {
        "num_rows": table.num_rows,
        "size_mb": (table.num_bytes / (1024 * 1024)) if table.num_bytes else 0.0,
        "description": table.description or "",
        "schema": schema,
    }


# === HELPERS =======================================================

def _format_size_mb(size_mb: float) -> str:
    if size_mb is None:
        return "-"
    if size_mb >= 1024:
        return f"{size_mb / 1024:.2f} GB"
    return f"{size_mb:.2f} MB"


def _schema_to_dataframe(schema) -> pd.DataFrame:
    return pd.DataFrame(schema, columns=["column", "type", "mode"])


def _show_error(out: widgets.Output, exc: BaseException) -> None:
    with out:
        clear_output()
        msg = f"{type(exc).__name__}: {exc}"
        display(widgets.HTML(
            f"<pre style='color:#a00;background:#fff5f5;border:1px solid #f3c2c2;"
            f"padding:8px;border-radius:4px;white-space:pre-wrap;'>{msg}</pre>"
        ))


# === WIDGETS =======================================================
# Pure builders. They create widgets and lay them out, but attach no
# callbacks - the controller section wires those up.

def _section_header(text: str) -> widgets.HTML:
    return widgets.HTML(
        f"<h4 style='margin:8px 0 4px 0;border-bottom:1px solid #ddd;"
        f"padding-bottom:4px;'>{text}</h4>"
    )


def _build_connection_panel(initial_project: str = "", initial_dataset: str = "") -> dict:
    project_text = widgets.Text(
        value=initial_project,
        placeholder="my-gcp-project",
        description="Project ID:",
        layout=widgets.Layout(width="420px"),
        style={"description_width": "120px"},
    )
    dataset_text = widgets.Text(
        value=initial_dataset,
        placeholder="(optional) my_dataset",
        description="Dataset ID:",
        layout=widgets.Layout(width="420px"),
        style={"description_width": "120px"},
    )
    connect_btn = widgets.Button(description="Connect", button_style="primary")
    error_out = widgets.Output()
    box = widgets.VBox([
        _section_header("1. Connect"),
        project_text,
        dataset_text,
        connect_btn,
        error_out,
    ])
    return {
        "box": box,
        "project_text": project_text,
        "dataset_text": dataset_text,
        "connect_btn": connect_btn,
        "error_out": error_out,
    }


def _build_dataset_panel(dataset_ids) -> dict:
    select = widgets.Select(
        options=list(dataset_ids),
        value=None,
        rows=12,
        layout=widgets.Layout(width="420px"),
    )
    error_out = widgets.Output()
    box = widgets.VBox([
        _section_header(f"2. Datasets ({len(dataset_ids)})"),
        select,
        error_out,
    ])
    return {"box": box, "select": select, "error_out": error_out}


def _build_table_panel(table_ids) -> dict:
    select = widgets.Select(
        options=list(table_ids),
        value=None,
        rows=12,
        layout=widgets.Layout(width="420px"),
    )
    error_out = widgets.Output()
    box = widgets.VBox([
        _section_header(f"3. Tables ({len(table_ids)})"),
        select,
        error_out,
    ])
    return {"box": box, "select": select, "error_out": error_out}


def _build_data_panel(columns, default_rows: int) -> dict:
    rows_slider = widgets.IntSlider(
        value=default_rows,
        min=10,
        max=500,
        step=10,
        description="Rows to preview:",
        continuous_update=False,
        layout=widgets.Layout(width="500px"),
        style={"description_width": "140px"},
    )
    summary_out = widgets.Output()
    schema_out = widgets.Output()

    filter_text = widgets.Text(
        placeholder="Filter columns",
        description="Filter:",
        layout=widgets.Layout(width="320px"),
        style={"description_width": "60px"},
    )
    column_checkboxes = [
        widgets.Checkbox(value=True, description=c, indent=False,
                         layout=widgets.Layout(width="auto"))
        for c in columns
    ]
    columns_box = widgets.VBox(
        column_checkboxes,
        layout=widgets.Layout(
            max_height="220px", overflow_y="auto",
            border="1px solid #ddd", padding="4px", width="320px",
        ),
    )
    df_out = widgets.Output()

    box = widgets.VBox([
        _section_header("4. Data"),
        rows_slider,
        summary_out,
        widgets.HTML("<b>Schema</b>"),
        schema_out,
        widgets.HTML("<b>Columns</b> <span style='color:#888;font-size:90%'>"
                     "(filtering hides checkboxes; ticking/unticking updates the preview "
                     "without re-querying)</span>"),
        filter_text,
        columns_box,
        widgets.HTML("<b>Preview</b>"),
        df_out,
    ])
    return {
        "box": box,
        "rows_slider": rows_slider,
        "summary_out": summary_out,
        "schema_out": schema_out,
        "filter_text": filter_text,
        "columns_box": columns_box,
        "column_checkboxes": column_checkboxes,
        "df_out": df_out,
    }


# === CONTROLLER ====================================================
# Holds mutable state and wires widget events to BQ calls. Every
# handler is wrapped so that errors land in the relevant Output
# instead of bubbling up as a raw traceback.

class _ExplorerState:
    def __init__(self, default_rows: int = 20):
        self.client = None
        self.project_id: Optional[str] = None
        self.dataset_id: Optional[str] = None
        self.table_id: Optional[str] = None
        self.current_df: Optional[pd.DataFrame] = None
        self.default_rows = default_rows
        self.root = widgets.VBox([])
        self.panels: dict = {}
        self.global_err = widgets.Output()


def _append_panel(state: _ExplorerState, name: str, panel: dict) -> None:
    """Replace any panel with this name and any panels below it."""
    order = ["connection", "dataset", "table", "data"]
    if name not in order:
        raise ValueError(name)
    keep_until = order.index(name)
    new_children = []
    for n in order[:keep_until]:
        if n in state.panels:
            new_children.append(state.panels[n]["box"])
    new_children.append(panel["box"])
    state.panels = {n: state.panels[n] for n in order[:keep_until] if n in state.panels}
    state.panels[name] = panel
    state.root.children = tuple(new_children) + (state.global_err,)


def _safe(out: widgets.Output):
    """Decorator: run handler, route exceptions to `out`."""
    def deco(fn):
        def wrapped(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as e:
                _show_error(out, e)
        return wrapped
    return deco


def _on_connect_clicked(state: _ExplorerState, conn: dict, _btn=None) -> None:
    out = conn["error_out"]
    with out:
        clear_output()
    try:
        project_id = conn["project_text"].value.strip()
        dataset_id = conn["dataset_text"].value.strip() or None
        if not project_id:
            raise ValueError("Project ID is required.")
        _check_identifier(project_id, "project")
        if dataset_id:
            _check_identifier(dataset_id, "dataset")
        state.project_id = project_id
        state.dataset_id = dataset_id
        state.client = get_client(project_id)
        _load_datasets_or_jump(state)
    except Exception as e:
        _show_error(out, e)


def _load_datasets_or_jump(state: _ExplorerState) -> None:
    if state.dataset_id:
        _load_tables(state, state.dataset_id)
    else:
        _load_datasets(state)


def _load_datasets(state: _ExplorerState) -> None:
    try:
        dataset_ids = list_datasets(state.client, state.project_id)
    except Exception as e:
        _show_error(state.global_err, e)
        return
    panel = _build_dataset_panel(dataset_ids)
    _append_panel(state, "dataset", panel)
    panel["select"].observe(
        lambda change: _on_dataset_change(state, change), names="value"
    )


def _on_dataset_change(state: _ExplorerState, change) -> None:
    new = change.get("new") if isinstance(change, dict) else change.new
    if not new:
        return
    state.dataset_id = new
    _load_tables(state, new)


def _load_tables(state: _ExplorerState, dataset_id: str) -> None:
    err_out = state.panels.get("dataset", {}).get("error_out") or state.global_err
    try:
        table_ids = list_tables(state.client, state.project_id, dataset_id)
    except Exception as e:
        _show_error(err_out, e)
        return
    panel = _build_table_panel(table_ids)
    _append_panel(state, "table", panel)
    panel["select"].observe(
        lambda change: _on_table_change(state, change), names="value"
    )


def _on_table_change(state: _ExplorerState, change) -> None:
    new = change.get("new") if isinstance(change, dict) else change.new
    if not new:
        return
    state.table_id = new
    _load_data(state, initial=True)


def _load_data(state: _ExplorerState, initial: bool = False) -> None:
    """Fetch metadata + preview. Builds the data panel on first call;
    subsequent calls (slider change) just refresh the existing panel."""
    err_out = state.panels.get("table", {}).get("error_out") or state.global_err
    try:
        meta = get_table_metadata(
            state.client, state.project_id, state.dataset_id, state.table_id
        )
        limit = state.default_rows
        if "data" in state.panels:
            limit = state.panels["data"]["rows_slider"].value
        df = preview_table(
            state.client, state.project_id, state.dataset_id, state.table_id, limit
        )
    except Exception as e:
        _show_error(err_out, e)
        return

    state.current_df = df
    columns = list(df.columns)

    if initial or "data" not in state.panels:
        panel = _build_data_panel(columns, default_rows=state.default_rows)
        _append_panel(state, "data", panel)
        # Wire callbacks once.
        panel["rows_slider"].observe(
            lambda change: _on_rows_change(state, change), names="value"
        )
        panel["filter_text"].observe(
            lambda change: _on_filter_text_change(state, change), names="value"
        )
        for cb in panel["column_checkboxes"]:
            cb.observe(lambda change: _on_columns_change(state), names="value")
    else:
        panel = state.panels["data"]
        # Columns shouldn't change for the same table, but rebuild anyway
        # if the schema somehow shifted between calls.
        if [cb.description for cb in panel["column_checkboxes"]] != columns:
            new_checkboxes = [
                widgets.Checkbox(value=True, description=c, indent=False,
                                 layout=widgets.Layout(width="auto"))
                for c in columns
            ]
            for cb in new_checkboxes:
                cb.observe(lambda change: _on_columns_change(state), names="value")
            panel["column_checkboxes"] = new_checkboxes
            panel["columns_box"].children = tuple(new_checkboxes)

    _render_summary(panel["summary_out"], meta, state)
    _render_schema(panel["schema_out"], meta["schema"])
    _render_dataframe(state)


def _on_rows_change(state: _ExplorerState, change) -> None:
    err_out = state.panels["data"].get("df_out") or state.global_err
    try:
        new_limit = change.get("new") if isinstance(change, dict) else change.new
        df = preview_table(
            state.client, state.project_id, state.dataset_id,
            state.table_id, int(new_limit),
        )
        state.current_df = df
        _render_dataframe(state)
    except Exception as e:
        _show_error(err_out, e)


def _on_columns_change(state: _ExplorerState) -> None:
    _render_dataframe(state)


def _on_filter_text_change(state: _ExplorerState, change) -> None:
    panel = state.panels["data"]
    q = (change.get("new") if isinstance(change, dict) else change.new) or ""
    q = q.strip().lower()
    for cb in panel["column_checkboxes"]:
        match = (q == "") or (q in cb.description.lower())
        cb.layout.display = "" if match else "none"


def _render_summary(out: widgets.Output, meta: dict, state: _ExplorerState) -> None:
    with out:
        clear_output()
        rows = meta.get("num_rows")
        size = _format_size_mb(meta.get("size_mb"))
        desc = meta.get("description") or "(no description)"
        rows_str = f"{rows:,}" if rows is not None else "-"
        display(widgets.HTML(
            f"<div style='font-family:monospace;'>"
            f"<b>{state.project_id}.{state.dataset_id}.{state.table_id}</b><br>"
            f"Rows: {rows_str} &nbsp;|&nbsp; Size: {size}<br>"
            f"<span style='color:#555'>{desc}</span>"
            f"</div>"
        ))


def _render_schema(out: widgets.Output, schema) -> None:
    with out:
        clear_output()
        sdf = _schema_to_dataframe(schema)
        with pd.option_context("display.max_rows", None):
            display(sdf)


def _render_dataframe(state: _ExplorerState) -> None:
    panel = state.panels.get("data")
    if panel is None or state.current_df is None:
        return
    selected = [cb.description for cb in panel["column_checkboxes"] if cb.value]
    out = panel["df_out"]
    with out:
        clear_output()
        if not selected:
            display(widgets.HTML(
                "<i style='color:#888'>No columns selected.</i>"
            ))
            return
        display(state.current_df[selected])


# === ENTRYPOINT ====================================================

def explore(
    project_id: Optional[str] = None,
    dataset_id: Optional[str] = None,
    default_rows: int = 20,
):
    """Launch the interactive BigQuery explorer.

    project_id  - if provided, skip the project input field
    dataset_id  - if provided alongside project_id, jump straight to the
                  table list for that dataset
    default_rows - initial value of the row-count slider (10-500)
    """
    state = _ExplorerState(default_rows=max(10, min(500, int(default_rows))))
    state.root = widgets.VBox([state.global_err])
    display(state.root)

    if project_id is None:
        conn = _build_connection_panel(initial_dataset=dataset_id or "")
        _append_panel(state, "connection", conn)
        conn["connect_btn"].on_click(
            lambda btn: _on_connect_clicked(state, conn, btn)
        )
        return

    state.project_id = project_id
    state.dataset_id = dataset_id
    try:
        state.client = get_client(project_id)
    except Exception as e:
        _show_error(state.global_err, e)
        return
    _load_datasets_or_jump(state)


if __name__ == "__main__":
    # Triggered by `%run bq_explorer.py` in a Jupyter cell.
    explore()
