import pandas as pd


def get_filterable_columns(df, max_categorical_unique=50):
    """Identify which columns are eligible for filtering.

    Numeric columns are always eligible.
    Categorical columns are only eligible if they have <= max_categorical_unique
    unique values (a column with 500 unique IDs would make a useless filter).

    Returns a dict with "numeric" and "categorical" lists of column names.
    """
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = [
        col for col in df.select_dtypes(exclude="number").columns
        if df[col].nunique() <= max_categorical_unique
    ]
    return {"numeric": numeric_cols, "categorical": categorical_cols}


def apply_filters(df, numeric_filters, categorical_filters):
    """Apply all active filters to the DataFrame and return the filtered result.

    numeric_filters: dict of {column_name: (min_val, max_val)}
    categorical_filters: dict of {column_name: [selected_values]}

    An empty categorical selection means "no filter" (show all values).
    """
    filtered = df.copy()

    for col, (min_val, max_val) in numeric_filters.items():
        filtered = filtered[(filtered[col] >= min_val) & (filtered[col] <= max_val)]

    for col, selected_values in categorical_filters.items():
        if selected_values:
            filtered = filtered[filtered[col].isin(selected_values)]

    return filtered


def sort_dataframe(df, sort_column, ascending=True):
    """Sort the DataFrame by a single column.

    Returns the original DataFrame unchanged if sort_column is None.
    """
    if sort_column is None:
        return df
    return df.sort_values(by=sort_column, ascending=ascending, ignore_index=True)


def convert_df_to_csv(df):
    """Convert a DataFrame to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")
