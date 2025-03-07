# Analytics MCP Server

This MCP server enables Claude to perform data analysis on CSV files, allowing for powerful data exploration capabilities without requiring the user to write code.

## Features

The server provides three main tools:

1. **analyze_csv**: Generate various analysis reports for a CSV file
2. **filter_csv**: Filter a CSV file based on specified conditions and save the results
3. **group_by_analysis**: Perform group-by aggregation operations on CSV data

## Setup

### Prerequisites

- Python 3.10 or higher
- pandas and numpy libraries

### Installation

1. Install the required dependencies:
```bash
pip install -r ../requirements.txt
pip install pandas numpy
```

2. Add the server to your Claude Desktop configuration file:
```json
{
  "mcpServers": {
    "analytics": {
      "command": "python /absolute/path/to/claude-mcp-tools/analytics-server/server.py"
    }
  }
}
```

3. Restart Claude Desktop

## Usage Examples

Once configured, you can use the server through Claude Desktop by asking questions like:

- "Analyze the sales.csv file and give me a summary of the data"
- "Filter customers.csv to only include rows where the state is California"
- "Group the sales data by product category and calculate the sum and average of revenue"

## Available Tools and Parameters

### analyze_csv

Analyze a CSV file with various operations.

Parameters:
- `file_path`: Path to the CSV file to analyze
- `operations`: List of operations to perform. Options:
  - `"summary"`: General summary statistics
  - `"correlation"`: Correlation matrix for numeric columns
  - `"missing"`: Analysis of missing values
  - `"distribution"`: Distribution analysis for numeric columns

### filter_csv

Filter a CSV file based on a condition and save to a new file.

Parameters:
- `file_path`: Path to the CSV file to filter
- `column`: Column name to apply the filter on
- `condition`: Filter condition ('=', '!=', '>', '<', '>=', '<=', 'contains', 'startswith', 'endswith')
- `value`: Value to filter by
- `output_path`: Path to save the filtered CSV (optional, defaults to adding '_filtered' to original name)

### group_by_analysis

Perform a group-by analysis on a CSV file.

Parameters:
- `file_path`: Path to the CSV file to analyze
- `group_column`: Column to group by
- `agg_columns`: Columns to aggregate
- `agg_functions`: Aggregation functions to apply. Options: 'mean', 'sum', 'count', 'min', 'max', 'median'

## Example Workflows

### Basic Data Exploration

1. "Can you analyze the customer_data.csv file for me?"
2. "Great, now look at the correlation matrix to identify relationships between variables"
3. "Filter the data to only include customers with a purchase value greater than 1000"

### Segmentation Analysis

1. "Group the sales.csv data by customer_segment and calculate the mean and sum of revenue"
2. "Now filter to only high-value transactions over $5000 and save that to high_value.csv"
3. "Analyze the high_value.csv file and compare the distribution to the original dataset"

## Limitations

- The server can only analyze CSV files in a standard format
- Performance may be limited for very large CSV files
- All files must be accessible from the local filesystem
- Complex statistical analysis beyond the built-in functions is not supported

## License

This project is licensed under the MIT License.