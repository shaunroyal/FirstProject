# bq_explorer

A single-file interactive BigQuery browser for Jupyter notebooks running on
[Vertex AI Workbench](https://cloud.google.com/vertex-ai-workbench). Drop one
file into your notebook, run a cell, and click around your BigQuery datasets
and tables with no SQL required for browsing.

## What is this?

`bq_explorer.py` gives you a small UI inside a Jupyter cell. You pick a
project, then a dataset, then a table, and the script previews the rows and
schema for you. You can change how many rows to preview, hide columns you
don't care about, and search through the column list. Behind the scenes it
uses the `google-cloud-bigquery` client and `ipywidgets` — both of which are
preinstalled on Vertex AI Workbench managed notebooks, so there is **nothing
to install**.

The whole thing is one file. There is no package, no `pip install`, no setup.

## Before you start

You need:

1. **A Vertex AI Workbench notebook** (or any Jupyter environment where
   Application Default Credentials are configured).
2. **A GCP project with BigQuery enabled.**
3. **`bigquery.dataViewer`** (or stronger) on whatever datasets you want to
   browse, plus `bigquery.jobUser` to run preview queries. If you can already
   query a table in the BigQuery web UI, you have enough access.

## Quick start

You have three ways to load the script. Pick whichever is easiest.

### Option A — paste the file next to your notebook

1. Save `bq_explorer.py` in the same folder as your `.ipynb` notebook.
2. In a notebook cell run:

    ```python
    %run bq_explorer.py
    ```

   The UI will appear immediately and walk you through the steps.

### Option B — import it

If you'd rather call it explicitly:

```python
from bq_explorer import explore
explore()
```

This works as long as `bq_explorer.py` is in the same directory as your
notebook (or anywhere on `sys.path`).

### Option C — pull it from GCS at runtime

Handy if you keep the script in a shared bucket so a team can use the same
copy:

```python
!gsutil cp gs://YOUR_BUCKET/bq_explorer.py .
%run bq_explorer.py
```

## Using the UI

The UI builds itself up panel by panel as you make selections. You'll see at
most four sections stacked vertically.

1. **Connect** — type the GCP project ID you want to browse. If you already
   know which dataset you want, type its name in the optional dataset field
   and you'll skip ahead. Click **Connect** to initialise the BigQuery
   client.
2. **Datasets** — a scrollable list of every dataset in the project. Click
   one to load its tables.
3. **Tables** — a scrollable list of every table in the selected dataset.
   Click one to load a preview.
4. **Data** — this is where the action is:
   - A **Rows to preview** slider (10–500). Drag it and a new query runs.
   - A summary line with the fully-qualified table name, total row count,
     size, and the table description (if any).
   - A **Schema** mini-table showing each column's name, type, and mode
     (`NULLABLE` / `REQUIRED` / `REPEATED`).
   - A **Filter** text box and a scrollable list of column checkboxes. Type
     in the filter to narrow which checkboxes are visible. Untick a column
     and the preview updates instantly — this is purely a display change,
     so it does **not** re-run the BigQuery query.
   - The **Preview** itself, rendered as a pandas DataFrame.

## Calling `explore()` with arguments

You can skip parts of the UI by passing arguments:

```python
# 1. Fully guided — type everything in the UI
explore()

# 2. Project is fixed, browse datasets interactively
explore(project_id="my-gcp-project")

# 3. Jump straight to a specific dataset's tables
explore(project_id="my-gcp-project", dataset_id="my_dataset")

# Set a different default for the rows slider (clamped to 10–500)
explore(project_id="my-gcp-project", default_rows=100)
```

## Troubleshooting

**"Could not automatically determine credentials"**
You're probably running outside Vertex AI Workbench. On a local machine run
`gcloud auth application-default login` in a terminal once, then retry. On
Workbench this should never happen — if it does, the notebook may have been
started with a service account that has no BigQuery permissions.

**"403 Access Denied" or "User does not have permission"**
Your account doesn't have BigQuery access to the dataset. Ask your GCP admin
for the `roles/bigquery.dataViewer` role on the dataset (or the project) and
`roles/bigquery.jobUser` on the project.

**The widgets show up as the literal text `Widget(...)`**
Your notebook frontend isn't rendering ipywidgets. On Vertex Workbench this
is enabled by default; elsewhere try:

```bash
pip install --upgrade ipywidgets
```

then **restart the kernel** (not just re-run the cell).

**Nothing happens when I click a dataset/table**
Look for a red error box just under the list — most BigQuery errors (timeouts,
permission denied, table not found) surface there as friendly messages
instead of as a Python traceback.

## What it does NOT do

This is a read-only browser. It does not:

- Run arbitrary SQL — it only runs `SELECT * ... LIMIT N` for previews
- Modify, delete, or create any tables, datasets, or rows
- Export data to GCS or anywhere else
- Cache results — every slider change re-queries BigQuery (so previews
  count against your query quota)

If you need any of those, use the BigQuery web console or the
`google-cloud-bigquery` Python client directly.
