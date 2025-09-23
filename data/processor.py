import pandas as pd
import numpy as np
from typing import Union, Any

class DataProcessor:
    """Main data processing class for handling imputation and transformations."""
    
    def __init__(self):
        self.supported_methods = ['mean', 'median', 'mode', 'custom', 'drop']
    
    def apply_imputation(self, df: pd.DataFrame, column: str, method: str, custom_value: Any = None) -> pd.DataFrame:
        """
        Apply imputation method to a specific column.
        
        Args:
            df: DataFrame to process
            column: Column name to impute
            method: Imputation method ('mean', 'median', 'mode', 'custom', 'drop')
            custom_value: Custom value to use if method is 'custom'
            
        Returns:
            DataFrame with imputation applied
        """
        if method not in self.supported_methods:
            raise ValueError(f"Unsupported method: {method}")
        
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
        
        df_copy = df.copy()
        
        if method == 'drop':
            # Drop rows with missing values in this column
            df_copy = df_copy.dropna(subset=[column])
        
        elif method == 'mean':
            if not pd.api.types.is_numeric_dtype(df_copy[column]):
                raise ValueError(f"Cannot apply mean imputation to non-numeric column: {column}")
            fill_value = df_copy[column].mean()
            df_copy[column] = df_copy[column].fillna(fill_value)
        
        elif method == 'median':
            if not pd.api.types.is_numeric_dtype(df_copy[column]):
                raise ValueError(f"Cannot apply median imputation to non-numeric column: {column}")
            fill_value = df_copy[column].median()
            df_copy[column] = df_copy[column].fillna(fill_value)
        
        elif method == 'mode':
            mode_values = df_copy[column].mode()
            if len(mode_values) > 0:
                fill_value = mode_values.iloc[0]
                df_copy[column] = df_copy[column].fillna(fill_value)
        
        elif method == 'custom':
            if custom_value is None:
                raise ValueError("Custom value must be provided when using custom imputation method")
            
            # Convert custom value to appropriate type
            if pd.api.types.is_numeric_dtype(df_copy[column]):
                try:
                    custom_value = float(custom_value)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid numeric value for column {column}: {custom_value}")
            
            df_copy[column] = df_copy[column].fillna(custom_value)
        
        return df_copy
    
    def get_column_statistics(self, df: pd.DataFrame, column: str) -> dict:
        """
        Get basic statistics for a column.
        
        Args:
            df: DataFrame
            column: Column name
            
        Returns:
            Dictionary with statistics
        """
        if column not in df.columns:
            return {}
        
        series = df[column]
        stats = {
            'column': column,
            'dtype': str(series.dtype),
            'missing_count': series.isnull().sum(),
            'missing_percentage': (series.isnull().sum() / len(series)) * 100,
            'non_null_count': series.count()
        }
        
        if pd.api.types.is_numeric_dtype(series):
            stats.update({
                'mean': series.mean(),
                'median': series.median(),
                'std': series.std(),
                'min': series.min(),
                'max': series.max()
            })
        
        # Mode (works for both numeric and categorical)
        try:
            mode_values = series.mode()
            if len(mode_values) > 0:
                stats['mode'] = mode_values.iloc[0]
        except:
            pass
        
        return stats
    
    def validate_dataframe(self, df: pd.DataFrame) -> dict:
        """
        Validate DataFrame and return quality metrics.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Dictionary with validation results
        """
        return {
            'shape': df.shape,
            'total_cells': df.shape[0] * df.shape[1],
            'missing_cells': df.isnull().sum().sum(),
            'missing_percentage': (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100,
            'columns_with_missing': df.columns[df.isnull().any()].tolist(),
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict()
        }