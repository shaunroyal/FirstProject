# Data Quality Management Tool

A comprehensive multi-file Plotly Dash application for data quality assessment and automated imputation of missing values in CSV datasets.

## Features

### 🔍 Data Quality Assessment
- **Upload CSV datasets** with drag-and-drop functionality
- **Comprehensive data summary** including:
  - Dataset dimensions (rows/columns)
  - Missing value counts and percentages
  - Data type breakdown
  - Basic statistical summaries
  - Data preview with pagination

### 🛠️ Smart Imputation Methods
- **Mean imputation** for normally distributed numeric data
- **Median imputation** for skewed numeric data
- **Mode imputation** for categorical data
- **Custom value imputation** for domain-specific requirements
- **Row deletion** for high missing value scenarios

### 📊 Interactive User Interface
- **Column-by-column imputation selection** with intelligent method recommendations
- **Real-time statistics** showing mean, median, and mode values
- **Custom value inputs** with type validation
- **Responsive design** that works on desktop and mobile

### 📈 Transformation Logging
- **Complete audit trail** of all transformations applied
- **Timestamp tracking** for each operation
- **Method and parameter logging** for reproducibility
- **Export capabilities** for transformation reports

### 💾 Export Functionality
- **Download cleaned datasets** as CSV files
- **Generate transformation reports** with detailed summaries
- **Before/after comparisons** in comprehensive reports

## Project Structure

```
FirstProject/
├── app.py                     # Main Dash application entry point
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── components/               # UI components
│   ├── __init__.py
│   ├── upload.py            # File upload component
│   ├── summary.py           # Data summary display
│   └── imputation.py        # Imputation controls
├── data/                    # Data processing modules
│   ├── __init__.py
│   ├── processor.py         # Core data processing and imputation
│   └── logger.py           # Transformation logging
├── utils/                   # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Helper functions and validators
└── assets/                  # Static assets
    └── style.css           # Custom CSS styling
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd FirstProject
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser** and navigate to `http://127.0.0.1:8050`

## Usage Guide

### Step 1: Upload Your Dataset
1. Click on the upload area or drag and drop a CSV file
2. The application will automatically parse and validate your data
3. View the comprehensive data quality summary

### Step 2: Review Data Quality
- **Dataset Overview**: Check rows, columns, and missing value statistics
- **Data Types**: Review the distribution of data types in your dataset
- **Missing Values**: Identify columns with missing data and their percentages
- **Data Preview**: Browse the first 10 rows of your dataset

### Step 3: Configure Imputation Methods
1. For each column with missing values:
   - **Review statistics**: Mean, median, and mode values are displayed
   - **Select method**: Choose from available imputation methods
   - **Custom values**: Enter specific values if using custom imputation
   - **Method recommendations**: The app suggests optimal methods based on data distribution

### Step 4: Apply Transformations
1. Click "Apply Transformations" to process your data
2. All changes are logged with timestamps and parameters
3. Review the transformation summary

### Step 5: Export Results
- **Download Cleaned Dataset**: Get your processed CSV file
- **Download Transformation Report**: Get a detailed report of all changes made

## Imputation Methods Explained

### Numeric Data
- **Mean**: Best for normally distributed data without outliers
- **Median**: Robust against outliers and skewed distributions
- **Mode**: For discrete numeric data with clear patterns
- **Custom**: When domain knowledge suggests specific values

### Categorical Data
- **Mode**: Most frequent category (default recommendation)
- **Custom**: Specific category based on business logic

### Universal Options
- **Drop Rows**: Remove rows with missing values (use cautiously)

## Technical Details

### Core Dependencies
- **Dash 2.17.1**: Web application framework
- **Plotly 5.17.0**: Interactive visualizations
- **Pandas 2.1.4**: Data manipulation and analysis
- **NumPy 1.24.4**: Numerical computing
- **Dash Bootstrap Components**: UI components and styling

### Key Classes

#### `DataProcessor`
- Core data processing functionality
- Imputation method implementations
- Data validation and statistics

#### `TransformationLogger`
- Comprehensive logging of all transformations
- Export capabilities for audit trails
- Summary statistics for applied changes

#### Helper Functions
- File parsing and validation
- Data profiling and recommendations
- Formatting and display utilities

### Data Flow
1. **Upload** → File parsing and validation
2. **Analysis** → Data quality assessment and statistics
3. **Configuration** → User selects imputation methods
4. **Processing** → Apply transformations and log changes
5. **Export** → Download cleaned data and reports

## Error Handling

The application includes comprehensive error handling for:
- **Invalid file formats** (only CSV supported)
- **Encoding issues** (tries multiple encodings)
- **Data type mismatches** (validates custom values)
- **Method compatibility** (prevents invalid method/column combinations)
- **Empty datasets** and **missing columns**

## Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Performance Notes

- **Memory Usage**: Large datasets (>100MB) may require additional memory
- **Processing Time**: Complex imputations on large datasets may take several seconds
- **Browser Limits**: Very large datasets may hit browser memory limits

## Future Enhancements

Potential improvements for future versions:
- Support for additional file formats (Excel, JSON)
- Advanced imputation methods (KNN, regression-based)
- Data visualization for missing value patterns
- Batch processing capabilities
- Database connectivity
- Advanced data profiling and outlier detection

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions, please open an issue in the GitHub repository.