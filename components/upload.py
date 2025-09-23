import dash_bootstrap_components as dbc
from dash import dcc, html

def create_upload_component():
    """Create the file upload component."""
    return dbc.Card([
        dbc.CardBody([
            html.H4("Upload CSV Dataset", className="card-title"),
            html.P("Select a CSV file to analyze and clean", className="card-text"),
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    "Drag and Drop or ",
                    html.A("Select Files")
                ]),
                style={
                    "width": "100%",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px"
                },
                multiple=False,
                accept=".csv"
            )
        ])
    ])