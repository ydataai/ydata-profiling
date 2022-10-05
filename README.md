# `pandas-profiling`

![Pandas Profiling Logo Header](https://pandas-profiling.ydata.ai/docs/assets/logo_header.png)

[![Build Status](https://github.com/ydataai/pandas-profiling/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/ydataai/pandas-profiling/actions/workflows/tests.yml)
[![Code Coverage](https://codecov.io/gh/ydataai/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF)](https://codecov.io/gh/ydataai/pandas-profiling)
[![Release Version](https://img.shields.io/github/release/ydataai/pandas-profiling.svg)](https://github.com/ydataai/pandas-profiling/releases)
[![Python Version](https://img.shields.io/pypi/pyversions/pandas-profiling)](https://pypi.org/project/pandas-profiling/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)


<p align="center">
  <a href="https://pandas-profiling.ydata.ai/docs/master/">Documentation</a>
  |
  <a href="https://slack.datacentricai.community/">Slack</a>
  | 
  <a href="https://stackoverflow.com/questions/tagged/pandas-profiling">Stack Overflow</a>
  |
  <a href="https://pandas-profiling.ydata.ai/docs/master/pages/reference/changelog.html#changelog">Latest changelog</a>

</p>

<p align="center">
  Do you like this project? Show us your love and <a href="https://engage.ydata.ai">give feedback!</a>
</p>

`pandas-profiling` generates profile reports from a pandas `DataFrame`. The pandas `df.describe()` function is handy yet a little basic for exploratory data analysis. `pandas-profiling` extends pandas `DataFrame` with `df.profile_report()`, which automatically generates a standardized univariate and multivariate report for data understanding.

For each column, the following information (whenever relevant for the column type) is presented in an interactive HTML report:

- **Type inference**: detect the types of columns in a DataFrame
- **Essentials**: type, unique values, indication of missing values
- **Quantile statistics**: minimum value, Q1, median, Q3, maximum, range, interquartile range
- **Descriptive statistics**: mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
- **Most frequent and extreme values**
- **Histograms**: categorical and numerical
- **Correlations**: high correlation warnings, based on different correlation metrics (Spearman, Pearson, Kendall, Cramér’s V, Phik)
- **Missing values**: through counts, matrix, heatmap and dendrograms
- **Duplicate rows**: list of the most common duplicated rows
- **Text analysis**: most common categories (uppercase, lowercase, separator), scripts (Latin, Cyrillic) and blocks (ASCII, Cyrilic)
- **File and Image analysis**: file sizes, creation dates, dimensions, indication of truncated images and existence of EXIF metadata

The report contains three additional sections:

- **Overview**: mostly global details about the dataset (number of records, number of variables, overall missigness and duplicates, memory footprint)
- **Alerts**: a comprehensive and automatic list of potential data quality issues (high correlation, skewness, uniformity, zeros, missing values, constant values, between others)
- **Reproduction**: technical details about the analysis (time, version and configuration)


> ⚡ Looking for a Spark backend to profile large datasets? It's [work in progress](https://github.com/ydataai/pandas-profiling/projects/3).
> 
> ⌛ Interested in uncovering temporal patterns? Check out [popmon](https://github.com/ing-bank/popmon).

## ▶️ Quickstart

Start by loading your pandas `DataFrame` as you normally would, e.g. by using:

```python
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])
```

To generate the standard profiling report, merely run:

```python
profile = ProfileReport(df, title="Pandas Profiling Report")
```

### Using inside Jupyter Notebooks

There are two interfaces to consume the report inside a Jupyter notebook: through widgets and through an embedded HTML report.

<img alt="Notebook Widgets" src="https://pandas-profiling.ydata.ai/docs/master/assets/widgets.gif" width="800" />

The above is achieved by simply displaying the report as a set of widgets. In a Jupyter Notebook, run:

```python
profile.to_widgets()
```

The HTML report can be directly embedded in a cell in a similar fashion:

```python
profile.to_notebook_iframe()
```

<img alt="HTML" src="https://pandas-profiling.ydata.ai/docs/master/assets/iframe.gif" width="800" />

### Exporting the report to a file

To generate a HTML report file, save the `ProfileReport` to an object and use the `to_file()` function:

```python
profile.to_file("your_report.html")
```

Alternatively, the report's data can be obtained as a JSON file:

```python
# As a JSON string
json_data = profile.to_json()

# As a file
profile.to_file("your_report.json")
```

### Using in the command line

For standard formatted CSV files (which can be read directly by pandas without additional settings), the `pandas_profiling` executable can be used in the command line. The example below generates a report named _Example Profiling Report_, using a configuration file called `default.yaml`, in the file `report.html` by processing a `data.csv` dataset.

```sh
pandas_profiling --title "Example Profiling Report" --config_file default.yaml data.csv report.html
```

Additional details on the CLI are available [on the documentation](https://pandas-profiling.ydata.ai/docs/master/pages/getting_started/quickstart.html#command-line-usage).

## 👀 Examples

The following example reports showcase the potentialities of the package across a wide range of dataset and data types:

* [Census Income](https://pandas-profiling.ydata.ai/examples/master/census/census_report.html) (US Adult Census data relating income with other demographic properties)
* [NASA Meteorites](https://pandas-profiling.ydata.ai/examples/master/meteorites/meteorites_report.html) (comprehensive set of meteorite landing - object properties and locations) [![Open In Colab](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/ydataai/pandas-profiling/blob/master/examples/meteorites/meteorites.ipynb) [![Binder](https://camo.githubusercontent.com/483bae47a175c24dfbfc57390edd8b6982ac5fb3/68747470733a2f2f6d7962696e6465722e6f72672f62616467655f6c6f676f2e737667)](https://mybinder.org/v2/gh/ydataai/pandas-profiling/master?filepath=examples%2Fmeteorites%2Fmeteorites.ipynb)
* [Titanic](https://pandas-profiling.ydata.ai/examples/master/titanic/titanic_report.html) (the "Wonderwall" of datasets) [![Open In Colab](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/ydataai/pandas-profiling/blob/master/examples/titanic/titanic.ipynb) [![Binder](https://camo.githubusercontent.com/483bae47a175c24dfbfc57390edd8b6982ac5fb3/68747470733a2f2f6d7962696e6465722e6f72672f62616467655f6c6f676f2e737667)](https://mybinder.org/v2/gh/ydataai/pandas-profiling/master?filepath=examples%2Ftitanic%2Ftitanic.ipynb)
* [NZA](https://pandas-profiling.ydata.ai/examples/master/nza/nza_report.html) (open data from the Dutch Healthcare Authority)
* [Stata Auto](https://pandas-profiling.ydata.ai/examples/master/stata_auto/stata_auto_report.html) (1978 Automobile data)
* [Colors](https://pandas-profiling.ydata.ai/examples/master/colors/colors_report.html) (a simple colors dataset)
* [Vektis](https://pandas-profiling.ydata.ai/examples/master/vektis/vektis_report.html) (Vektis Dutch Healthcare data)
* [UCI Bank Dataset](https://pandas-profiling.ydata.ai/examples/master/bank_marketing_data/uci_bank_marketing_report.html) (marketing dataset from a bank)
* [Russian Vocabulary](https://pandas-profiling.ydata.ai/examples/master/features/russian_vocabulary.html) (100 most common Russian words, showcasing unicode text analysis)
* [Website Inaccessibility](https://pandas-profiling.ydata.ai/examples/master/features/website_inaccessibility_report.html) (website accessibility analysis, showcasing support for URL data)
* [Orange prices](https://pandas-profiling.ydata.ai/examples/master/features/united_report.html) and [Coal prices](https://pandas-profiling.ydata.ai/examples/master/features/flatly_report.html) (simple pricing evolution datasets, showcasing the theming options)

## 🛠️ Installation

Additional details, including information about widget support, are available [on the documentation](https://pandas-profiling.ydata.ai/docs/master/pages/getting_started/installation.html).

### Using pip
[![PyPi Downloads](https://pepy.tech/badge/pandas-profiling)](https://pepy.tech/project/pandas-profiling)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-profiling/month)](https://pepy.tech/project/pandas-profiling/month)
[![PyPi Version](https://badge.fury.io/py/pandas-profiling.svg)](https://pypi.org/project/pandas-profiling/)

You can install using the `pip` package manager by running:

```sh
pip install -U pandas-profiling[notebook]
```

### Using conda
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pandas-profiling.svg)](https://anaconda.org/conda-forge/pandas-profiling)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pandas-profiling.svg)](https://anaconda.org/conda-forge/pandas-profiling) 


You can install using the `conda` package manager by running:

```sh
conda install -c conda-forge pandas-profiling
```

### From source (development)

Download the source code by cloning the repository or click on [Download ZIP](https://github.com/ydataai/pandas-profiling/archive/master.zip) to download the latest stable version.

Install it by navigating to the proper directory and running:

```sh
python setup.py install
```

The profiling report is written in HTML and CSS, which means a modern browser is required. 

You need [Python 3](https://python3statement.org/) to run the package. Other dependencies can be found in the requirements files:

| Filename | Requirements|
|----------|-------------|
| [requirements.txt](https://github.com/ydataai/pandas-profiling/blob/master/requirements.txt) | Package requirements|
| [requirements-dev.txt](https://github.com/ydataai/pandas-profiling/blob/master/requirements-dev.txt)  |  Requirements for development|
| [requirements-test.txt](https://github.com/ydataai/pandas-profiling/blob/master/requirements-test.txt) | Requirements for testing|
| [setup.py](https://github.com/ydataai/pandas-profiling/blob/master/setup.py) | Requirements for widgets etc. |

## 📝 Use cases

The documentation includes guides, tips and tricks for tackling common use cases:

| Use case | Description |
|---|---|
| [Profiling large datasets](https://pandas-profiling.ydata.ai/docs/master/pages/use_cases/big_data.html ) | Tips on how to prepare data and configure `pandas-profiling` for working with large datasets |
| [Handling sensitive data](https://pandas-profiling.ydata.ai/docs/master/pages/use_cases/sensitive_data.html ) | Generating reports which are mindful about sensitive data in the input dataset |
| [Dataset metadata and data dictionaries](https://pandas-profiling.ydata.ai/docs/master/pages/use_cases/metadata.html) | Complementing the report with dataset details and column-specific data dictionaries |
| [Customizing the report's appearance](https://pandas-profiling.ydata.ai/docs/master/pages/use_cases/custom_report_appearance.html ) | Changing the appearance of the report's page and of the contained visualizations |

## 🔗 Integrations

To maximize its usefulness in real world contexts, `pandas-profiling` has a set of implicit and explicit integrations with a variety of other actors in the Data Science ecosystem: 

| Integration type | Description |
|---|---|
| [Other DataFrame libraries](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/other_dataframe_libraries.html) | How to compute the profiling of data stored in libraries other than pandas |
| [Great Expectations](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/great_expectations.html) | Generating [Great Expectations](https://greatexpectations.io) expectations suites directly from a profiling report |
| [Interactive applications](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/data_apps.html) | Embedding profiling reports in [Streamlit](http://streamlit.io), [Dash](http://dash.plotly.com) or [Panel](https://panel.holoviz.org) applications |
| [Pipelines](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/pipelines.html) | Integration with DAG workflow execution tools like [Airflow](https://airflow.apache.org) or [Kedro](https://kedro.org) |
| [Cloud services](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/cloud_services.html) | Using `pandas-profiling` in hosted computation services like [Lambda](https://lambdalabs.com), [Google Cloud](https://github.com/GoogleCloudPlatform/analytics-componentized-patterns/blob/master/retail/propensity-model/bqml/bqml_kfp_retail_propensity_to_purchase.ipynb) or [Kaggle](https://www.kaggle.com/code) |
| [IDEs](https://pandas-profiling.ydata.ai/docs/master/pages/integrations/ides.html) | Using `pandas-profiling` directly from integrated development environments such as [PyCharm](https://www.jetbrains.com/pycharm/) |

## 🙋 Support
Need help? Want to share a perspective? Report a bug? Ideas for collaborations? Reach out via the following channels:

- [Stack Overflow](https://stackoverflow.com/questions/tagged/pandas-profiling): ideal for asking questions on how to use the package
- [GitHub Issues](https://github.com/ydataai/pandas-profiling/issues): bugs, proposals for changes, feature requests
- [Slack](https://slack.datacentricai.community): general chat, questions, collaborations
- [Email](mailto:developers@ydata.ai): project collaborations or sponsoring

> ❗ Before reporting an issue on GitHub, check out [Common Issues](https://pandas-profiling.ydata.ai/docs/master/pages/support_contrib/common_issues.html).

## 🤝🏽 Contributing

Learn how to get involved in the [Contribution Guide](https://pandas-profiling.ydata.ai/docs/master/pages/support_contrib/contribution_guidelines.html).

A low-threshold place to ask questions or start contributing is the [Data Centric AI Community's Slack](https://slack.datacentricai.community).
