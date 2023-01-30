import kaggle
import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.paths import get_data_path

# The dataset in this example is obtained using the `kaggle` api.
# If you haven't done so already, you should set up the api credentials:
# https://github.com/Kaggle/kaggle-api#api-credentials
kaggle.api.authenticate()


# Download the dataset. Note that we use a small dataset as this example is automated.
# However, popular larger files shouldn't be a problem (LFW, CelebA).
data_path = get_data_path() / "celebrity-faces"
kaggle.api.dataset_download_files(
    "dansbecker/5-celebrity-faces-dataset",
    path=str(data_path),
    quiet=False,
    unzip=True,
)

p = data_path / "data/train/"

# As not all datasets have an index of files, we generate that ourselves.
files = [f for f in p.rglob("*") if f.is_file()]
series = pd.Series(files, name="files")
# PP only accepts absolute paths
series = series.apply(lambda x: x.absolute()).apply(str)

df = pd.DataFrame(series)

# Generate the profile report
profile = ProfileReport(
    df,
    title="Example showcasing EXIF data (Kaggle 5 Celebrity Faces Dataset)",
    # Disable what's not in our focus
    duplicates=None,
    correlations=None,
    samples=None,
    missing_diagrams=None,
    # Enable files and images (off by default, as it uses relatively expensive computations when not interested)
    explorative=True,
)
# We can also configure the report like this
profile.config.variables.descriptions = {
    "files": "The 5 Celebrity Faces Dataset found on Kaggle (dansbecker/5-celebrity-faces-dataset)."
}

# Save the report
profile.to_file("celebrity-faces.html")

# The analysis reveals that quite some photos contain "hidden" EXIF information.
# This can be both interesting as troublesome, depending on the situation.
