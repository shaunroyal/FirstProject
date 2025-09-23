import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd

def create_imputation_component(df):
    """Create the imputation controls component."""
    
    # Get columns with missing values
    missing_cols = df.columns[df.isnull().any()].tolist()
    
    if not missing_cols:
        return dbc.Alert("No missing values to impute!", color="success")
    
    return dbc.Card([
        dbc.CardBody([
            html.H4("Imputation Methods", className="card-title"),
            html.P("Select imputation methods for each column with missing values:", className="card-text"),
            
            html.Div([
                create_column_imputation_control(df, col, i) 
                for i, col in enumerate(missing_cols)
            ]),
            
            html.Hr(),
            dbc.Button(
                "Apply Transformations", 
                id="apply-transformations", 
                color="success", 
                size="lg",
                className="w-100"
            )
        ])
    ])

def create_column_imputation_control(df, column, index):
    """Create imputation control for a single column."""
    
    # Determine column type
    col_dtype = df[column].dtype
    is_numeric = pd.api.types.is_numeric_dtype(col_dtype)
    
    # Create method options based on column type
    if is_numeric:
        method_options = [
            {"label": "Mean", "value": "mean"},
            {"label": "Median", "value": "median"},
            {"label": "Mode", "value": "mode"},
            {"label": "Custom Value", "value": "custom"},
            {"label": "Drop Rows", "value": "drop"}
        ]
    else:
        method_options = [
            {"label": "Mode", "value": "mode"},
            {"label": "Custom Value", "value": "custom"},
            {"label": "Drop Rows", "value": "drop"}
        ]
    
    # Get some statistics for display
    missing_count = df[column].isnull().sum()
    missing_percentage = (missing_count / len(df)) * 100
    
    # Get current statistics
    stats_info = []
    if is_numeric:
        try:
            mean_val = df[column].mean()
            median_val = df[column].median()
            stats_info = [
                f"Mean: {mean_val:.2f}" if not pd.isna(mean_val) else "Mean: N/A",
                f"Median: {median_val:.2f}" if not pd.isna(median_val) else "Median: N/A"
            ]
        except:
            pass
    
    try:
        mode_val = df[column].mode()
        if len(mode_val) > 0:
            stats_info.append(f"Mode: {mode_val.iloc[0]}")
    except:
        pass
    
    return dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H6(f"{column}", className="text-primary"),
                    html.Small(f"Type: {col_dtype} | Missing: {missing_count} ({missing_percentage:.1f}%)", 
                              className="text-muted"),
                    html.Br(),
                    html.Small(" | ".join(stats_info), className="text-info") if stats_info else None
                ], width=4),
                dbc.Col([
                    dcc.Dropdown(
                        id=f"imputation-{index}",
                        options=method_options,
                        placeholder="Select imputation method...",
                        value=None
                    )
                ], width=4),
                dbc.Col([
                    dcc.Input(
                        id=f"custom-value-{index}",
                        type="number" if is_numeric else "text",
                        placeholder="Custom value (if selected)",
                        disabled=True,
                        style={"width": "100%"}
                    )
                ], width=4)
            ])
        ])
    ], className="mb-3")

# Note: The callback to enable/disable custom input would be handled in the main app