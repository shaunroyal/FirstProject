from datetime import datetime
from typing import List, Dict, Any, Optional

class TransformationLogger:
    """Logger for tracking data transformations and imputation operations."""
    
    def __init__(self):
        self.log_entries: List[Dict[str, Any]] = []
    
    def log_transformation(self, column: str, method: str, custom_value: Optional[Any] = None, 
                          additional_info: Optional[Dict[str, Any]] = None):
        """
        Log a transformation operation.
        
        Args:
            column: Column name that was transformed
            method: Imputation method used
            custom_value: Custom value if applicable
            additional_info: Additional information about the transformation
        """
        entry = {
            'timestamp': datetime.now().isoformat(),
            'column': column,
            'method': method,
            'custom_value': custom_value,
            'additional_info': additional_info or {}
        }
        
        self.log_entries.append(entry)
    
    def get_log(self) -> List[Dict[str, Any]]:
        """Get all log entries."""
        return self.log_entries.copy()
    
    def get_log_for_column(self, column: str) -> List[Dict[str, Any]]:
        """Get log entries for a specific column."""
        return [entry for entry in self.log_entries if entry['column'] == column]
    
    def clear_log(self):
        """Clear all log entries."""
        self.log_entries.clear()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all transformations."""
        if not self.log_entries:
            return {
                'total_transformations': 0,
                'columns_affected': [],
                'methods_used': [],
                'first_transformation': None,
                'last_transformation': None
            }
        
        columns_affected = list(set(entry['column'] for entry in self.log_entries))
        methods_used = list(set(entry['method'] for entry in self.log_entries))
        
        return {
            'total_transformations': len(self.log_entries),
            'columns_affected': columns_affected,
            'methods_used': methods_used,
            'first_transformation': self.log_entries[0]['timestamp'],
            'last_transformation': self.log_entries[-1]['timestamp']
        }
    
    def export_log(self, format: str = 'text') -> str:
        """
        Export log in specified format.
        
        Args:
            format: Export format ('text', 'csv', 'json')
            
        Returns:
            Formatted log string
        """
        if format == 'text':
            return self._export_as_text()
        elif format == 'csv':
            return self._export_as_csv()
        elif format == 'json':
            import json
            return json.dumps(self.log_entries, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_as_text(self) -> str:
        """Export log as formatted text."""
        if not self.log_entries:
            return "No transformations logged."
        
        lines = ["Data Transformation Log", "=" * 25, ""]
        
        for i, entry in enumerate(self.log_entries, 1):
            lines.append(f"{i}. Column: {entry['column']}")
            lines.append(f"   Method: {entry['method']}")
            lines.append(f"   Timestamp: {entry['timestamp']}")
            
            if entry.get('custom_value') is not None:
                lines.append(f"   Custom Value: {entry['custom_value']}")
            
            if entry.get('additional_info'):
                lines.append(f"   Additional Info: {entry['additional_info']}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _export_as_csv(self) -> str:
        """Export log as CSV format."""
        if not self.log_entries:
            return "timestamp,column,method,custom_value,additional_info\n"
        
        lines = ["timestamp,column,method,custom_value,additional_info"]
        
        for entry in self.log_entries:
            custom_val = entry.get('custom_value', '')
            additional_info = str(entry.get('additional_info', ''))
            
            lines.append(f"{entry['timestamp']},{entry['column']},{entry['method']},{custom_val},{additional_info}")
        
        return "\n".join(lines)