"""Utils for pandas DataFrames."""
import pandas as pd


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


def expand_mixed(df: pd.DataFrame, types=None) -> pd.DataFrame:
    """Expand non-nested lists, dicts and tuples in a DataFrame into columns with a prefix.

    Args:
        types: list of types to expand (Default: list, dict, tuple)
        df: DataFrame

    Returns:
        DataFrame with the dict values as series, identifier by the combination of the series and dict keys.

    Notes:
        TODO: allow for list expansion by duplicating rows.
        TODO: allow for expansion of nested data structures.
    """
    if types is None:
        types = [list, dict, tuple]

    for column_name in df.columns:
        # All
        non_nested_enumeration = (
            df[column_name]
            .dropna()
            .map(lambda x: type(x) in types and not any(type(y) in types for y in x))
        )

        if non_nested_enumeration.all():
            # Expand and prefix
            expanded = pd.DataFrame(df[column_name].dropna().tolist())
            expanded = expanded.add_prefix(column_name + "_")

            # Add recursion
            expanded = expand_mixed(expanded)

            # Drop te expanded
            df.drop(columns=[column_name], inplace=True)

            df = pd.concat([df, expanded], axis=1)
    return df
