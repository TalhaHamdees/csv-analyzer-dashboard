"""Data profiling utilities for column analysis and datetime detection.

Pure pandas functions with no Streamlit dependencies, so they can be
tested independently. Caching is handled by wrapper functions in app.py.
"""

import pandas as pd


def get_column_info(df):
    """Build a summary table with one row per column in the DataFrame."""
    column_info = pd.DataFrame({
        "Data Type": df.dtypes.astype(str),
        "Non-Null Count": df.count(),
        "Missing Count": df.isnull().sum(),
        "Missing %": (df.isnull().sum() / len(df) * 100).round(2),
        "Unique Values": df.nunique()
    })
    return column_info


def get_numeric_stats(df):
    """Return descriptive statistics for numeric columns only.

    Returns None if the DataFrame has no numeric columns.
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty:
        return None
    # .T (transpose) flips rows/columns so each column becomes a row — easier to read
    return numeric_df.describe().T


def get_categorical_stats(df):
    """Return descriptive statistics for non-numeric (categorical) columns.

    Returns None if the DataFrame has no categorical columns.
    """
    categorical_df = df.select_dtypes(exclude="number")
    if categorical_df.empty:
        return None
    # include='all' ensures describe() works on text columns (not just numeric)
    return categorical_df.describe(include="all").T


def detect_datetime_columns(df, sample_size=100):
    """Identify columns that contain date/time values.

    Samples the first sample_size rows for speed, then confirms on the full
    column. A column qualifies if 50%+ of non-null values parse as dates.

    Returns a list of column names (empty list if none found).
    """
    datetime_cols = []

    for col in df.columns:
        # Already a datetime column — include directly
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            datetime_cols.append(col)
            continue

        # Only try parsing non-numeric columns (numbers aren't dates)
        if pd.api.types.is_numeric_dtype(df[col]):
            continue

        # Skip columns with no data
        non_null = df[col].dropna()
        if len(non_null) == 0:
            continue

        # Quick check on a sample first
        sample = non_null.head(sample_size)
        parsed_sample = pd.to_datetime(sample, errors="coerce")
        sample_success_rate = parsed_sample.notna().sum() / len(sample)

        if sample_success_rate < 0.5:
            continue

        # Sample passed — confirm on the full column
        parsed_full = pd.to_datetime(non_null, errors="coerce")
        full_success_rate = parsed_full.notna().sum() / len(non_null)

        if full_success_rate >= 0.5:
            datetime_cols.append(col)

    return datetime_cols
