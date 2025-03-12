import importlib

# List of modules in the 'pandas' model that should be imported explicitly
PANDAS_MODULES = [
    "correlations_pandas",
    "describe_generic_pandas",
    "describe_boolean_pandas",
    "describe_categorical_pandas",
    "describe_url_pandas",
    "describe_file_pandas",
    "describe_text_pandas",
    "describe_timeseries_pandas",
    "describe_numeric_pandas",
    "describe_path_pandas",
    "describe_image_pandas",
    "describe_date_pandas",
    "describe_counts_pandas",
    "duplicates_pandas",
    "sample_pandas",
    "table_pandas",
    "timeseries_index_pandas",
    "summary_pandas",
]

# Dynamically import and expose functions from modules
for module_name in PANDAS_MODULES:
    module = importlib.import_module(f"ydata_profiling.model.pandas.{module_name}")
    globals().update(
        {
            name: getattr(module, name)
            for name in dir(module)
            if not name.startswith("_")
        }
    )

# Explicitly list exposed names for clarity
__all__ = [
    "pandas_describe_generic",
    "pandas_describe_boolean_1d",
    "pandas_describe_categorical_1d",
    "pandas_describe_url_1d",
    "pandas_describe_file_1d",
    "pandas_describe_text_1d",
    "pandas_describe_timeseries_1d",
    "pandas_describe_numeric_1d",
    "pandas_describe_path_1d",
    "pandas_describe_image_1d",
    "pandas_describe_date_1d",
    "pandas_describe_counts",
    "pandas_get_duplicates",
    "pandas_get_sample",
    "pandas_get_table_stats",
    "pandas_get_time_index_description",
    "pandas_get_series_descriptions",
]
