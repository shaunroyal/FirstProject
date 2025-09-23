import base64
import io
import pandas as pd
from typing import Optional, Union

def parse_uploaded_file(contents: str, filename: str) -> pd.DataFrame:
    """
    Parse uploaded file contents and return DataFrame.
    
    Args:
        contents: Base64 encoded file contents
        filename: Name of the uploaded file
        
    Returns:
        Parsed DataFrame
        
    Raises:
        ValueError: If file format is not supported or parsing fails
    """
    if not filename.lower().endswith('.csv'):
        raise ValueError("Only CSV files are supported")
    
    try:
        # Decode the base64 encoded contents
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Try to read as CSV with different encodings
        encodings = ['utf-8', 'latin1', 'cp1252']
        
        for encoding in encodings:
            try:
                df = pd.read_csv(io.StringIO(decoded.decode(encoding)))
                return df
            except UnicodeDecodeError:
                continue
        
        # If all encodings fail, raise an error
        raise ValueError("Unable to decode file with supported encodings")
        
    except Exception as e:
        raise ValueError(f"Error parsing CSV file: {str(e)}")

def validate_csv_structure(df: pd.DataFrame) -> dict:
    """
    Validate CSV structure and return validation results.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results
    """
    validation_results = {
        'is_valid': True,
        'issues': [],
        'warnings': [],
        'info': {}
    }
    
    # Check if DataFrame is empty
    if df.empty:
        validation_results['is_valid'] = False
        validation_results['issues'].append("DataFrame is empty")
        return validation_results
    
    # Check for completely empty columns
    empty_columns = df.columns[df.isnull().all()].tolist()
    if empty_columns:
        validation_results['warnings'].append(f"Completely empty columns: {empty_columns}")
    
    # Check for duplicate column names
    duplicate_columns = df.columns[df.columns.duplicated()].tolist()
    if duplicate_columns:
        validation_results['issues'].append(f"Duplicate column names: {duplicate_columns}")
        validation_results['is_valid'] = False
    
    # Check for columns with mixed data types (potential data quality issues)
    mixed_type_columns = []
    for col in df.select_dtypes(include=['object']).columns:
        try:
            # Try to convert to numeric - if it partially succeeds, it's mixed
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            if numeric_series.notna().sum() > 0 and numeric_series.isna().sum() > 0:
                mixed_type_columns.append(col)
        except:
            pass
    
    if mixed_type_columns:
        validation_results['warnings'].append(f"Columns with mixed data types: {mixed_type_columns}")
    
    # Add general info
    validation_results['info'] = {
        'shape': df.shape,
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
        'data_types': df.dtypes.value_counts().to_dict(),
        'missing_data_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    }
    
    return validation_results

def format_number(number: Union[int, float], precision: int = 2) -> str:
    """
    Format number for display with appropriate precision and thousand separators.
    
    Args:
        number: Number to format
        precision: Decimal precision for floats
        
    Returns:
        Formatted number string
    """
    if pd.isna(number):
        return "N/A"
    
    if isinstance(number, int) or number.is_integer():
        return f"{int(number):,}"
    else:
        return f"{number:,.{precision}f}"

def get_column_recommendations(df: pd.DataFrame, column: str) -> dict:
    """
    Get imputation method recommendations for a column based on its characteristics.
    
    Args:
        df: DataFrame
        column: Column name
        
    Returns:
        Dictionary with recommendations
    """
    if column not in df.columns:
        return {"error": "Column not found"}
    
    series = df[column]
    missing_count = series.isnull().sum()
    missing_percentage = (missing_count / len(series)) * 100
    
    recommendations = {
        'column': column,
        'missing_percentage': missing_percentage,
        'recommended_methods': [],
        'reasoning': []
    }
    
    # No missing values
    if missing_count == 0:
        recommendations['recommended_methods'] = ['none']
        recommendations['reasoning'] = ['No missing values detected']
        return recommendations
    
    # High missing percentage - recommend dropping
    if missing_percentage > 50:
        recommendations['recommended_methods'] = ['drop']
        recommendations['reasoning'].append(f'High missing percentage ({missing_percentage:.1f}%) - consider dropping rows')
    
    # Numeric columns
    if pd.api.types.is_numeric_dtype(series):
        # Check distribution for mean vs median recommendation
        try:
            skewness = series.skew()
            if abs(skewness) < 0.5:  # Roughly normal distribution
                recommendations['recommended_methods'].append('mean')
                recommendations['reasoning'].append('Normal distribution detected - mean imputation recommended')
            else:
                recommendations['recommended_methods'].append('median')
                recommendations['reasoning'].append('Skewed distribution detected - median imputation recommended')
        except:
            recommendations['recommended_methods'].extend(['mean', 'median'])
            recommendations['reasoning'].append('Consider mean or median based on distribution')
    
    # Categorical columns or object types
    else:
        recommendations['recommended_methods'].append('mode')
        recommendations['reasoning'].append('Categorical data - mode imputation recommended')
    
    # Always include custom as an option
    recommendations['recommended_methods'].append('custom')
    recommendations['reasoning'].append('Custom value option available for domain-specific imputation')
    
    return recommendations

def generate_data_profile(df: pd.DataFrame) -> dict:
    """
    Generate a comprehensive data profile.
    
    Args:
        df: DataFrame to profile
        
    Returns:
        Dictionary with data profile information
    """
    profile = {
        'overview': {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_cells': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100,
            'duplicate_rows': df.duplicated().sum(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024
        },
        'columns': {},
        'data_types': df.dtypes.value_counts().to_dict()
    }
    
    # Profile each column
    for col in df.columns:
        col_profile = {
            'dtype': str(df[col].dtype),
            'missing_count': df[col].isnull().sum(),
            'missing_percentage': (df[col].isnull().sum() / len(df)) * 100,
            'unique_count': df[col].nunique(),
            'unique_percentage': (df[col].nunique() / len(df)) * 100
        }
        
        # Add statistics for numeric columns
        if pd.api.types.is_numeric_dtype(df[col]):
            col_profile.update({
                'mean': df[col].mean(),
                'median': df[col].median(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
                'zeros_count': (df[col] == 0).sum()
            })
        
        # Add mode for all columns
        try:
            mode_values = df[col].mode()
            if len(mode_values) > 0:
                col_profile['mode'] = mode_values.iloc[0]
                col_profile['mode_frequency'] = (df[col] == mode_values.iloc[0]).sum()
        except:
            pass
        
        profile['columns'][col] = col_profile
    
    return profile