import importlib

# Dynamically import all modules inside the Spark folder
SPARK_MODULES = [
    "correlations_spark",
    "dataframe_spark",
    "describe_boolean_spark",
    "describe_categorical_spark",
    "describe_counts_spark",
    "describe_date_spark",
    "describe_generic_spark",
    "describe_numeric_spark",
    "describe_supported_spark",
    "duplicates_spark",
    "missing_spark",
    "sample_spark",
    "summary_spark",
    "table_spark",
    "timeseries_index_spark",
    "describe_text_spark",
]

# Load modules dynamically
for module_name in SPARK_MODULES:
    module = importlib.import_module(f"ydata_profiling.model.spark.{module_name}")
    globals().update(
        {
            name: getattr(module, name)
            for name in dir(module)
            if not name.startswith("_")
        }
    )  # type: ignore

# Explicitly list all available functions
__all__ = [
    "describe_generic_spark",
    "describe_boolean_1d_spark",
    "describe_categorical_1d_spark",
    "describe_text_1d_spark",
    "describe_numeric_1d_spark",
    "describe_date_1d_spark",
    "describe_counts_spark",
    "get_duplicates_spark",
    "get_sample_spark",
    "get_table_stats_spark",
    "get_time_index_description_spark",
    "get_series_descriptions_spark",
]
