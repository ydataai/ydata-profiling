import great_expectations as ge
import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

file_name = cache_file(
    "titanic.csv",
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
)

df = pd.read_csv(file_name)

profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

# Example 1
# Obtain expectation suite, this includes profiling the dataset, saving the expectation suite, validating the
# dataframe, and building data docs
suite = profile.to_expectation_suite(suite_name="titanic_expectations")

# Example 2
# Run Great Expectations while specifying the directory with an existing Great Expectations set-up by passing in a
# Data Context
data_context = ge.data_context.DataContext(context_root_dir="my_ge_root_directory/")

suite = profile.to_expectation_suite(
    suite_name="titanic_expectations", data_context=data_context
)

# Example 3
# Just build the suite
suite = profile.to_expectation_suite(
    suite_name="titanic_expectations",
    save_suite=False,
    run_validation=False,
    build_data_docs=False,
)

# Example 4
# If you would like to use the method to just build the suite, and then manually save the suite, validate the dataframe,
# and build data docs

# First instantiate a data_context
data_context = ge.data_context.DataContext(context_root_dir="my_ge_root_directory/")

# Create the suite
suite = profile.to_expectation_suite(
    suite_name="titanic_expectations",
    data_context=data_context,
    save_suite=False,
    run_validation=False,
    build_data_docs=False,
)

# Save the suite
data_context.save_expectation_suite(suite)

# Run validation on your dataframe
batch = ge.dataset.PandasDataset(df, expectation_suite=suite)

results = data_context.run_validation_operator(
    "action_list_operator", assets_to_validate=[batch]
)
validation_result_identifier = results.list_validation_result_identifiers()[0]

# Build and open data docs
data_context.build_data_docs()
data_context.open_data_docs(validation_result_identifier)
