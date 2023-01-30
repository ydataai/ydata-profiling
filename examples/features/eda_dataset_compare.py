import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    # Read the Titanic Dataset
    file_name = cache_file(
        "titanic.csv",
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
    )
    df = pd.read_csv(file_name)

    # Generate the Profiling Report from 2 samples from titanic dataset
    profile1 = ProfileReport(df.sample(frac=0.5))
    profile2 = ProfileReport(df.sample(frac=0.5))

    # compare the profiles and generate a comparison profile
    comparison = profile1.compare(profile2)
    comparison.to_file("profile_comparison.html")
