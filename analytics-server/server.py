from typing import Any, List, Optional, Dict
import pandas as pd
import numpy as np
import json
import tempfile
import io
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("analytics")

@mcp.tool()
async def analyze_csv(file_path: str, operations: List[str] = ["summary"]) -> str:
    """Analyze a CSV file with various operations.
    
    Args:
        file_path: Path to the CSV file to analyze
        operations: List of operations to perform. Options:
            - "summary": General summary statistics
            - "correlation": Correlation matrix for numeric columns
            - "missing": Analysis of missing values
            - "distribution": Distribution analysis for numeric columns
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        results = []
        
        # Process each requested operation
        for operation in operations:
            if operation.lower() == "summary":
                results.append(get_summary_stats(df))
            
            elif operation.lower() == "correlation":
                results.append(get_correlation_matrix(df))
            
            elif operation.lower() == "missing":
                results.append(analyze_missing_values(df))
            
            elif operation.lower() == "distribution":
                results.append(analyze_distributions(df))
            
            else:
                results.append(f"Unknown operation: {operation}")
        
        return "\n\n".join(results)
    
    except Exception as e:
        return f"Error analyzing CSV file: {str(e)}"

@mcp.tool()
async def filter_csv(file_path: str, column: str, condition: str, value: Any, output_path: Optional[str] = None) -> str:
    """Filter a CSV file based on a condition and save to a new file.
    
    Args:
        file_path: Path to the CSV file to filter
        column: Column name to apply the filter on
        condition: Filter condition ('=', '!=', '>', '<', '>=', '<=', 'contains', 'startswith', 'endswith')
        value: Value to filter by
        output_path: Path to save the filtered CSV (optional, defaults to adding '_filtered' to original name)
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Apply the filter based on the condition
        if condition == "=":
            filtered_df = df[df[column] == value]
        elif condition == "!=":
            filtered_df = df[df[column] != value]
        elif condition == ">":
            filtered_df = df[df[column] > float(value)]
        elif condition == "<":
            filtered_df = df[df[column] < float(value)]
        elif condition == ">=":
            filtered_df = df[df[column] >= float(value)]
        elif condition == "<=":
            filtered_df = df[df[column] <= float(value)]
        elif condition.lower() == "contains":
            filtered_df = df[df[column].astype(str).str.contains(str(value), na=False)]
        elif condition.lower() == "startswith":
            filtered_df = df[df[column].astype(str).str.startswith(str(value), na=False)]
        elif condition.lower() == "endswith":
            filtered_df = df[df[column].astype(str).str.endswith(str(value), na=False)]
        else:
            return f"Unknown condition: {condition}"
        
        # Determine the output path
        if not output_path:
            base, ext = os.path.splitext(file_path)
            output_path = f"{base}_filtered{ext}"
        
        # Save the filtered data
        filtered_df.to_csv(output_path, index=False)
        
        return f"Filtered CSV saved to {output_path}. {len(filtered_df)} rows match the filter criteria out of {len(df)} total rows."
    
    except Exception as e:
        return f"Error filtering CSV file: {str(e)}"

@mcp.tool()
async def group_by_analysis(file_path: str, group_column: str, agg_columns: List[str], agg_functions: List[str] = ["mean"]) -> str:
    """Perform a group-by analysis on a CSV file.
    
    Args:
        file_path: Path to the CSV file to analyze
        group_column: Column to group by
        agg_columns: Columns to aggregate
        agg_functions: Aggregation functions to apply. Options: 'mean', 'sum', 'count', 'min', 'max', 'median'
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Validate agg_functions
        valid_functions = ["mean", "sum", "count", "min", "max", "median"]
        agg_dict = {}
        
        for col in agg_columns:
            funcs = []
            for func in agg_functions:
                if func.lower() in valid_functions:
                    funcs.append(func.lower())
            if funcs:
                agg_dict[col] = funcs
        
        if not agg_dict:
            return "No valid aggregation functions specified."
        
        # Perform the group-by operation
        grouped = df.groupby(group_column).agg(agg_dict)
        
        # Convert the result to a string representation
        buffer = io.StringIO()
        grouped.to_string(buffer)
        
        return f"Group by analysis for {group_column}:\n\n{buffer.getvalue()}"
    
    except Exception as e:
        return f"Error performing group-by analysis: {str(e)}"

def get_summary_stats(df: pd.DataFrame) -> str:
    """Generate summary statistics for a DataFrame."""
    # Get basic info
    num_rows, num_cols = df.shape
    column_info = df.dtypes.to_dict()
    
    # Get summary statistics for numeric columns
    numeric_stats = df.describe().transpose()
    
    # Format the results
    result = f"CSV Summary Statistics\n{'='*50}\n"
    result += f"Rows: {num_rows}, Columns: {num_cols}\n\n"
    
    result += "Column Types:\n"
    for col, dtype in column_info.items():
        result += f"- {col}: {dtype}\n"
    
    result += "\nNumeric Statistics:\n"
    buffer = io.StringIO()
    numeric_stats.to_string(buffer)
    result += buffer.getvalue()
    
    return result

def get_correlation_matrix(df: pd.DataFrame) -> str:
    """Generate a correlation matrix for numeric columns."""
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=[np.number])
    
    if numeric_cols.empty:
        return "No numeric columns found for correlation analysis."
    
    # Calculate correlation matrix
    corr_matrix = numeric_cols.corr()
    
    # Format the result
    result = f"Correlation Matrix\n{'='*50}\n"
    buffer = io.StringIO()
    corr_matrix.to_string(buffer)
    result += buffer.getvalue()
    
    return result

def analyze_missing_values(df: pd.DataFrame) -> str:
    """Analyze missing values in the DataFrame."""
    # Count missing values per column
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df)) * 100
    
    # Format the result
    result = f"Missing Values Analysis\n{'='*50}\n"
    
    for col, count in missing_counts.items():
        if count > 0:
            result += f"- {col}: {count} missing values ({missing_percentage[col]:.2f}%)\n"
    
    if missing_counts.sum() == 0:
        result += "No missing values found in the dataset."
    else:
        result += f"\nTotal missing values: {missing_counts.sum()} ({missing_counts.sum() / (df.shape[0] * df.shape[1]) * 100:.2f}% of all data)"
    
    return result

def analyze_distributions(df: pd.DataFrame) -> str:
    """Analyze distributions of numeric columns."""
    # Select only numeric columns
    numeric_cols = df.select_dtypes(include=[np.number])
    
    if numeric_cols.empty:
        return "No numeric columns found for distribution analysis."
    
    # Calculate distribution statistics
    result = f"Distribution Analysis\n{'='*50}\n"
    
    for col in numeric_cols.columns:
        series = df[col].dropna()
        result += f"\n{col}:\n"
        result += f"- Range: {series.min()} to {series.max()}\n"
        result += f"- Mean: {series.mean():.4f}\n"
        result += f"- Median: {series.median():.4f}\n"
        result += f"- Mode: {series.mode()[0]:.4f}\n"
        result += f"- Standard Deviation: {series.std():.4f}\n"
        result += f"- Skewness: {series.skew():.4f}\n"
        result += f"- Kurtosis: {series.kurtosis():.4f}\n"
        
        # Get quantiles
        quantiles = series.quantile([0.25, 0.5, 0.75])
        result += f"- 25th Percentile: {quantiles[0.25]:.4f}\n"
        result += f"- 50th Percentile: {quantiles[0.5]:.4f}\n"
        result += f"- 75th Percentile: {quantiles[0.75]:.4f}\n"
    
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
