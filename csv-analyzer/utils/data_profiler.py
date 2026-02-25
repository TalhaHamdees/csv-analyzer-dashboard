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
