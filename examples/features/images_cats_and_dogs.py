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
data_path = get_data_path() / "cat-and-dog"
kaggle.api.dataset_download_files(
    "tongpython/cat-and-dog",
    path=str(data_path),
    quiet=False,
    unzip=True,
)

# At the first run, we find that the dataset not only contains images, "_DS_Store" and "cat-and-dog.zip" are present too.
# We remove these by narrowing our glob search
files = [f for f in data_path.rglob("*.jpg") if f.is_file()]
series = pd.Series(files, name="files")

# PP only accepts absolute paths
series = series.apply(lambda x: x.absolute()).apply(str)

df = pd.DataFrame(series)

# Generate the profile report
profile = ProfileReport(
    df,
    title="Example of summarization of an image dataset (Kaggle Cat and Dog dataset)",
    # We will not need those
    samples=None,
    missing_diagrams=None,
)

# Give our variable a description
profile.config.variables.descriptions = {
    "files": "Paths linking to the cats and dogs found https://www.kaggle.com/tongpython/cat-and-dog."
}

# If the number of samples is above this threshold, the scatter plots are replaced with hexbin plots
# We are just over the threshold of 10.000 samples, so let's increase the limit.
profile.config.plot.scatter_threshold = 25000

# Enable files and images (off by default, as it uses relatively expensive computations when not interested)
profile.config.vars.path.active = True
profile.config.vars.file.active = True
profile.config.vars.image.active = True

# No exif found, so turn off expensive computation
profile.config.vars.image.exif = False

# Save the report to a file
profile.to_file("cats-and-dogs.html")

# The scatter plot is interesting to look at.
# Find it here: "Image" > Dimensions > Scatter plot.

# Summarizing, using EDA we found that the directory not only contains images, but also few other files (.zip and DS_STORE)
# After that, we learned that images ave been processed so that their largest dimension is 500, with two outliers.
# We can fix these issues and then continue exploring our data in more depth!
