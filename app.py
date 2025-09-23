import dash
from dash import html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import io
import base64
import json
from datetime import datetime

from components.upload import create_upload_component
from components.summary import create_summary_component
from components.imputation import create_imputation_component
from data.processor import DataProcessor
from data.logger import TransformationLogger
from utils.helpers import parse_uploaded_file

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Data Quality Management Tool"

# Initialize data processor and logger
data_processor = DataProcessor()
transformation_logger = TransformationLogger()

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Data Quality Management Tool", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Upload section
    dbc.Row([
        dbc.Col([
            create_upload_component()
        ])
    ], className="mb-4"),
    
    # Data summary section
    dbc.Row([
        dbc.Col([
            html.Div(id="data-summary")
        ])
    ], className="mb-4"),
    
    # Imputation controls section
    dbc.Row([
        dbc.Col([
            html.Div(id="imputation-controls")
        ])
    ], className="mb-4"),
    
    # Export section
    dbc.Row([
        dbc.Col([
            html.Div(id="export-section")
        ])
    ], className="mb-4"),
    
    # Hidden divs to store data
    html.Div(id="stored-data", style={"display": "none"}),
    html.Div(id="processed-data", style={"display": "none"}),
    html.Div(id="transformation-log", style={"display": "none"})
], fluid=True)

# Callback for file upload
@app.callback(
    [Output("stored-data", "children"),
     Output("data-summary", "children")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def handle_file_upload(contents, filename):
    if contents is None:
        return "", ""
    
    try:
        # Parse uploaded file
        df = parse_uploaded_file(contents, filename)
        
        # Store data
        stored_data = df.to_json(date_format='iso', orient='split')
        
        # Create summary
        summary = create_summary_component(df)
        
        return stored_data, summary
    
    except Exception as e:
        return "", dbc.Alert(f"Error processing file: {str(e)}", color="danger")

# Callback for imputation controls
@app.callback(
    Output("imputation-controls", "children"),
    [Input("stored-data", "children")]
)
def show_imputation_controls(stored_data):
    if not stored_data:
        return ""
    
    try:
        df = pd.read_json(stored_data, orient='split')
        return create_imputation_component(df)
    except:
        return ""

# Callback for applying transformations
@app.callback(
    [Output("processed-data", "children"),
     Output("transformation-log", "children"),
     Output("export-section", "children")],
    [Input("apply-transformations", "n_clicks")],
    [State("stored-data", "children"),
     State("imputation-controls", "children")]
)
def apply_transformations(n_clicks, stored_data, imputation_controls):
    if not n_clicks or not stored_data:
        return "", "", ""
    
    try:
        df = pd.read_json(stored_data, orient='split')
        
        # Get column names with missing values
        missing_cols = df.columns[df.isnull().any()].tolist()
        
        # For now, we'll use a simpler approach - this can be enhanced later
        # Apply basic mean/median/mode imputation for demonstration
        processed_df = df.copy()
        
        for col in missing_cols:
            if pd.api.types.is_numeric_dtype(processed_df[col]):
                # Use median for numeric columns
                fill_value = processed_df[col].median()
                processed_df[col] = processed_df[col].fillna(fill_value)
                transformation_logger.log_transformation(col, "median", fill_value)
            else:
                # Use mode for categorical columns
                mode_values = processed_df[col].mode()
                if len(mode_values) > 0:
                    fill_value = mode_values.iloc[0]
                    processed_df[col] = processed_df[col].fillna(fill_value)
                    transformation_logger.log_transformation(col, "mode", fill_value)
        
        # Store processed data
        processed_data = processed_df.to_json(date_format='iso', orient='split')
        
        # Get transformation log
        log_data = json.dumps(transformation_logger.get_log())
        
        # Create export section
        export_section = create_export_section()
        
        return processed_data, log_data, export_section
    
    except Exception as e:
        return "", "", dbc.Alert(f"Error applying transformations: {str(e)}", color="danger")

def create_export_section():
    return dbc.Card([
        dbc.CardBody([
            html.H4("Export Options", className="card-title"),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Download Cleaned Dataset", id="download-csv", color="primary", className="me-2"),
                    dcc.Download(id="download-csv-file")
                ], width=6),
                dbc.Col([
                    dbc.Button("Download Transformation Report", id="download-report", color="secondary"),
                    dcc.Download(id="download-report-file")
                ], width=6)
            ])
        ])
    ])

# Callback for CSV download
@app.callback(
    Output("download-csv-file", "data"),
    [Input("download-csv", "n_clicks")],
    [State("processed-data", "children")]
)
def download_csv(n_clicks, processed_data):
    if not n_clicks or not processed_data:
        return dash.no_update
    
    df = pd.read_json(processed_data, orient='split')
    return dcc.send_data_frame(df.to_csv, "cleaned_dataset.csv", index=False)

# Callback for report download
@app.callback(
    Output("download-report-file", "data"),
    [Input("download-report", "n_clicks")],
    [State("transformation-log", "children"),
     State("stored-data", "children"),
     State("processed-data", "children")]
)
def download_report(n_clicks, log_data, original_data, processed_data):
    if not n_clicks or not log_data:
        return dash.no_update
    
    # Generate report
    report = generate_transformation_report(log_data, original_data, processed_data)
    return dict(content=report, filename="transformation_report.txt")

def generate_transformation_report(log_data, original_data, processed_data):
    log = json.loads(log_data)
    original_df = pd.read_json(original_data, orient='split')
    processed_df = pd.read_json(processed_data, orient='split')
    
    report = []
    report.append("Data Quality Transformation Report")
    report.append("=" * 40)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    
    report.append("Original Dataset Summary:")
    report.append(f"- Shape: {original_df.shape}")
    report.append(f"- Missing values: {original_df.isnull().sum().sum()}")
    report.append("")
    
    report.append("Processed Dataset Summary:")
    report.append(f"- Shape: {processed_df.shape}")
    report.append(f"- Missing values: {processed_df.isnull().sum().sum()}")
    report.append("")
    
    report.append("Transformations Applied:")
    for entry in log:
        report.append(f"- Column '{entry['column']}': {entry['method']}")
        if entry.get('custom_value'):
            report.append(f"  Custom value: {entry['custom_value']}")
        report.append(f"  Timestamp: {entry['timestamp']}")
        report.append("")
    
    return "\n".join(report)

if __name__ == "__main__":
    app.run_server(debug=True)