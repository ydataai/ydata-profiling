"""Utils for pandas DataFrames."""


def clean_column_names(df):
    """Removes spaces and colons from pandas DataFrame column names

    Args:
        df: DataFrame

    Returns:
        DataFrame with spaces in column names replaced by underscores, colons removed.
    """
    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace(":", "")
    return df


def rename_index(df):
    """If the DataFrame contains a column or index named `index`, this will produce errors. We rename the {index,column}
    to be `df_index`.

    Args:
        df: DataFrame to process.

    Returns:
        The DataFrame with {index,column} `index` replaced by `df_index`, unchanged if the DataFrame does not contain such a string.
    """
    df.rename(columns={"index": "df_index"}, inplace=True)

    if "index" in df.index.names:
        df.index.names = [x if x != "index" else "df_index" for x in df.index.names]
    return df
