"""Utils for pandas DataFrames."""
import warnings
from pathlib import Path

import joblib
import pandas as pd


def warn_read(extension):
    """Warn the user when an extension is not supported.

    Args:
        extension: The extension that is not supported.
    """
    warnings.warn(
        f"""There was an attempt to read a file with extension {extension}, we assume it to be in CSV format.
To prevent this warning from showing up, please rename the file to any of the extensions supported by pandas
(docs: https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html)
If you think this extension should be supported, please report this as an issue:
https://github.com/pandas-profiling/pandas-profiling/issues"""
    )


def read_pandas(file_name: Path) -> pd.DataFrame:
    """Read DataFrame based on the file extension. This function is used when the file is in a standard format.
    Various file types are supported (.csv, .json, .jsonl, .data, .tsv, .xls, .xlsx, .xpt, .sas7bdat, .parquet)

    Args:
        file_name: the file to read

    Returns:
        DataFrame

    Notes:
        This function is based on pandas IO tools:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html
        https://pandas.pydata.org/pandas-docs/stable/reference/io.html

        This function is not intended to be flexible or complete. The main use case is to be able to read files without
        user input, which is currently used in the editor integration. For more advanced use cases, the user should load
        the DataFrame in code.
    """
    extension = file_name.suffix.lower()
    if extension == ".json":
        df = pd.read_json(str(file_name))
    elif extension == ".jsonl":
        df = pd.read_json(str(file_name), lines=True)
    elif extension == ".dta":
        df = pd.read_stata(str(file_name))
    elif extension == ".tsv":
        df = pd.read_csv(str(file_name), sep="\t")
    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(str(file_name))
    elif extension in [".hdf", ".h5"]:
        df = pd.read_hdf(str(file_name))
    elif extension in [".sas7bdat", ".xpt"]:
        df = pd.read_sas(str(file_name))
    elif extension == ".parquet":
        df = pd.read_parquet(str(file_name))
    elif extension in [".pkl", ".pickle"]:
        df = pd.read_pickle(str(file_name))
    else:
        if extension != ".csv":
            warn_read(extension)

        df = pd.read_csv(str(file_name))
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


def hash_dataframe(df):
    """Hash a DataFrame (wrapper around joblib.hash, might change in the future)

    Args:
        df: the DataFrame

    Returns:
        The DataFrame's hash
    """
    return joblib.hash(df)
