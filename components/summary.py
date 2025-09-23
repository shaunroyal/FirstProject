import dash_bootstrap_components as dbc
from dash import html, dash_table
import pandas as pd

def create_summary_component(df):
    """Create the data summary component."""
    
    # Basic info
    n_rows, n_cols = df.shape
    missing_count = df.isnull().sum().sum()
    missing_percentage = (missing_count / (n_rows * n_cols)) * 100
    
    # Data types info
    dtype_counts = df.dtypes.value_counts()
    
    # Missing values per column
    missing_per_col = df.isnull().sum()
    missing_cols = missing_per_col[missing_per_col > 0]
    
    # Basic statistics for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    
    return dbc.Card([
        dbc.CardBody([
            html.H4("Data Quality Summary", className="card-title"),
            
            # Basic statistics
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{n_rows:,}", className="text-center text-primary mb-0"),
                            html.P("Rows", className="text-center text-muted mb-0")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{n_cols}", className="text-center text-info mb-0"),
                            html.P("Columns", className="text-center text-muted mb-0")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{missing_count:,}", className="text-center text-warning mb-0"),
                            html.P("Missing Values", className="text-center text-muted mb-0")
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5(f"{missing_percentage:.1f}%", className="text-center text-danger mb-0"),
                            html.P("Missing %", className="text-center text-muted mb-0")
                        ])
                    ])
                ], width=3)
            ], className="mb-4"),
            
            # Data types breakdown
            html.H5("Data Types"),
            html.Div([
                dbc.Badge(f"{dtype}: {count}", color="secondary", className="me-2")
                for dtype, count in dtype_counts.items()
            ], className="mb-4"),
            
            # Missing values breakdown
            html.H5("Columns with Missing Values"),
            html.Div([
                create_missing_values_table(missing_cols, n_rows) if len(missing_cols) > 0 
                else dbc.Alert("No missing values found!", color="success")
            ], className="mb-4"),
            
            # Data preview
            html.H5("Data Preview"),
            dash_table.DataTable(
                data=df.head(10).to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'padding': '10px',
                    'fontFamily': 'Arial'
                },
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                },
                page_size=10
            )
        ])
    ])

def create_missing_values_table(missing_cols, n_rows):
    """Create a table showing missing values per column."""
    missing_data = []
    for col, count in missing_cols.items():
        percentage = (count / n_rows) * 100
        missing_data.append({
            'Column': col,
            'Missing Count': f"{count:,}",
            'Missing %': f"{percentage:.1f}%"
        })
    
    return dash_table.DataTable(
        data=missing_data,
        columns=[
            {"name": "Column", "id": "Column"},
            {"name": "Missing Count", "id": "Missing Count"},
            {"name": "Missing %", "id": "Missing %"}
        ],
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontFamily': 'Arial'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )