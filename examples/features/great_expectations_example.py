import pandas as pd

from pandas_profiling import ProfileReport
from pandas_profiling.utils.cache import cache_file

file_name = cache_file(
    "titanic.csv",
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
)

df = pd.read_csv(file_name)

profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

# Obtain expectations suite, this includes profiling the dataset
suite = profile.to_expectations_suite()

# Or write directly as expectation suite json in GE
profile.to_expectations(suite_name="titanic_expectations")
