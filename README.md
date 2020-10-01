# Pandas Profiling

![Pandas Profiling Logo Header](https://pandas-profiling.github.io/pandas-profiling/docs/assets/logo_header.png)

[![Build Status](https://travis-ci.com/pandas-profiling/pandas-profiling.svg?branch=master)](https://travis-ci.com/pandas-profiling/pandas-profiling)
[![Code Coverage](https://codecov.io/gh/pandas-profiling/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF)](https://codecov.io/gh/pandas-profiling/pandas-profiling)
[![Release Version](https://img.shields.io/github/release/pandas-profiling/pandas-profiling.svg)](https://github.com/pandas-profiling/pandas-profiling/releases)
[![Python Version](https://img.shields.io/pypi/pyversions/pandas-profiling)](https://pypi.org/project/pandas-profiling/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)


<p align="center">
  <a href="https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/">Documentation</a>
  |
  <a href="https://join.slack.com/t/pandas-profiling/shared_invite/zt-hfy3iwp2-qEJSItye5QBZf8YGFMaMnQ">Slack</a>
  | 
  <a href="https://stackoverflow.com/questions/tagged/pandas-profiling">Stack Overflow</a>
</p>

Generates profile reports from a pandas `DataFrame`. 
The pandas `df.describe()` function is great but a little basic for serious exploratory data analysis. 
`pandas_profiling` extends the pandas DataFrame with `df.profile_report()` for quick data analysis.

For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:

* **Type inference**: detect the [types](#types) of columns in a dataframe.
* **Essentials**: type, unique values, missing values
* **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histogram**
* **Correlations** highlighting of highly correlated variables, Spearman, Pearson and Kendall matrices
* **Missing values** matrix, count, heatmap and dendrogram of missing values
* **Text analysis** learn about categories (Uppercase, Space), scripts (Latin, Cyrillic) and blocks (ASCII) of text data.
* **File and Image analysis** extract file sizes, creation dates and dimensions and scan for truncated images or those containing EXIF information.

## Announcements

### Version v2.9.0 released

The release candidate for v2.9.0 was already out for a while, now v2.9.0 is finally released. See the changelog below to know what has changed.

### Spark backend in progress

We can happily announce that we're working on a Spark backend for generating profile reports.
Stay tuned.

### Support `pandas-profiling`

The development of ``pandas-profiling`` relies completely on contributions.
If you find value in the package, we welcome you to support the project through [GitHub Sponsors](https://github.com/sponsors/sbrugman)!
It's extra exciting that GitHub **matches your contribution** for the first year.

Find more information here:

 - [Changelog v2.9.0](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/pages/changelog.html#changelog-v2-9-0)
 - [Sponsor the project on GitHub](https://github.com/sponsors/sbrugman)

 *September 2, 2020 💘*

---

_Contents:_ **[Examples](#examples)** |
**[Installation](#installation)** | **[Documentation](#documentation)** |
**[Large datasets](#large-datasets)** | **[Command line usage](#command-line-usage)** |
**[Advanced usage](#advanced-usage)** | **[Support](#supporting-open-source)** |
**[Types](#types)** | **[How to contribute](#contributing)** |
**[Editor Integration](#editor-integration)** | **[Dependencies](#dependencies)**

---

## Examples

The following examples can give you an impression of what the package can do:

* [Census Income](https://pandas-profiling.github.io/pandas-profiling/examples/master/census/census_report.html) (US Adult Census data relating income)
* [NASA Meteorites](https://pandas-profiling.github.io/pandas-profiling/examples/master/meteorites/meteorites_report.html) (comprehensive set of meteorite landings) [![Open In Colab](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/pandas-profiling/pandas-profiling/blob/master/examples/meteorites/meteorites.ipynb) [![Binder](https://camo.githubusercontent.com/483bae47a175c24dfbfc57390edd8b6982ac5fb3/68747470733a2f2f6d7962696e6465722e6f72672f62616467655f6c6f676f2e737667)](https://mybinder.org/v2/gh/pandas-profiling/pandas-profiling/master?filepath=examples%2Fmeteorites%2Fmeteorites.ipynb)
* [Titanic](https://pandas-profiling.github.io/pandas-profiling/examples/master/titanic/titanic_report.html) (the "Wonderwall" of datasets) [![Open In Colab](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/pandas-profiling/pandas-profiling/blob/master/examples/titanic/titanic.ipynb) [![Binder](https://camo.githubusercontent.com/483bae47a175c24dfbfc57390edd8b6982ac5fb3/68747470733a2f2f6d7962696e6465722e6f72672f62616467655f6c6f676f2e737667)](https://mybinder.org/v2/gh/pandas-profiling/pandas-profiling/master?filepath=examples%2Ftitanic%2Ftitanic.ipynb)
* [NZA](https://pandas-profiling.github.io/pandas-profiling/examples/master/nza/nza_report.html) (open data from the Dutch Healthcare Authority)
* [Stata Auto](https://pandas-profiling.github.io/pandas-profiling/examples/master/stata_auto/stata_auto_report.html) (1978 Automobile data)
* [Vektis](https://pandas-profiling.github.io/pandas-profiling/examples/master/vektis/vektis_report.html) (Vektis Dutch Healthcare data)
* [Colors](https://pandas-profiling.github.io/pandas-profiling/examples/master/colors/colors_report.html) (a simple colors dataset)
* [UCI Bank Dataset](https://pandas-profiling.github.io/pandas-profiling/examples/master/cbank_marketing_data/uci_bank_marketing_report.html) (banking marketing dataset)


Specific features:
* [Russian Vocabulary](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/russian_vocabulary.html) (demonstrates text analysis)
* [Cats and Dogs](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/cats-and-dogs.html) (demonstrates image analysis from the file system)
* [Celebrity Faces](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/celebrity-faces.html) (demonstrates image analysis with EXIF information)
* [Website Inaccessibility](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/website_inaccessibility_report.html) (demonstrates URL analysis)
* [Orange prices](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/united_report.html) and [Coal prices](https://pandas-profiling.github.io/pandas-profiling/examples/master/features/flatly_report.html) (showcases report themes)

Tutorials:
* [Tutorial: report structure using Kaggle data (advanced)](https://pandas-profiling.github.io/pandas-profiling/examples/master/tutorials/modify_report_structure.ipynb) (modify the report's structure) [![Open In Colab](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/pandas-profiling/pandas-profiling/blob/master/examples/tutorials/modify_report_structure.ipynb) [![Binder](https://camo.githubusercontent.com/483bae47a175c24dfbfc57390edd8b6982ac5fb3/68747470733a2f2f6d7962696e6465722e6f72672f62616467655f6c6f676f2e737667)](https://mybinder.org/v2/gh/pandas-profiling/pandas-profiling/master?filepath=examples%2Ftutorials%2Fmodify_report_structure.ipynb)


## Installation

### Using pip

[![PyPi Downloads](https://pepy.tech/badge/pandas-profiling)](https://pepy.tech/project/pandas-profiling)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-profiling/month)](https://pepy.tech/project/pandas-profiling/month)
[![PyPi Version](https://badge.fury.io/py/pandas-profiling.svg)](https://pypi.org/project/pandas-profiling/)

You can install using the pip package manager by running

    pip install pandas-profiling[notebook]
    
Alternatively, you could install the latest version directly from Github:

    pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip
    
    
### Using conda

[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/pandas-profiling.svg)](https://anaconda.org/conda-forge/pandas-profiling)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/pandas-profiling.svg)](https://anaconda.org/conda-forge/pandas-profiling) 
 
You can install using the conda package manager by running

    conda install -c conda-forge pandas-profiling

### From source

Download the source code by cloning the repository or by pressing ['Download ZIP'](https://github.com/pandas-profiling/pandas-profiling/archive/master.zip) on this page. 
Install by navigating to the proper directory and running

    python setup.py install
    
## Documentation

The documentation for `pandas_profiling` can be found [here](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/). Previous documentation is still available [here](https://pandas-profiling.github.io/pandas-profiling/docs/master/).

### Getting started

Start by loading in your pandas DataFrame, e.g. by using
```python
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.DataFrame(
    np.random.rand(100, 5),
    columns=["a", "b", "c", "d", "e"]
)
```
To generate the report, run:
```python
profile = ProfileReport(df, title="Pandas Profiling Report")
```

### Explore deeper

You can configure the profile report in any way you like. The example code below loads the [explorative configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_explorative.yaml), that includes many features for text (length distribution, unicode information), files (file size, creation time) and images (dimensions, exif information). If you are interested what exact settings were used, you can compare with the [default configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_default.yaml).

```python
profile = ProfileReport(df, title='Pandas Profiling Report', explorative=True)
```

Learn more about configuring `pandas-profiling` on the [Advanced usage](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/pages/advanced_usage.html) page.

#### Jupyter Notebook

We recommend generating reports interactively by using the Jupyter notebook. 
There are two interfaces (see animations below): through widgets and through a HTML report.

<img alt="Notebook Widgets" src="https://pandas-profiling.github.io/pandas-profiling/docs/master/assets/widgets.gif" width="800" />

This is achieved by simply displaying the report. In the Jupyter Notebook, run:
```python
profile.to_widgets()
```

The HTML report can be included in a Jupyter notebook:

<img alt="HTML" src="https://pandas-profiling.github.io/pandas-profiling/docs/master/assets/iframe.gif" width="800" />

Run the following code:

```python
profile.to_notebook_iframe()
```

#### Saving the report

If you want to generate a HTML report file, save the `ProfileReport` to an object and use the `to_file()` function:
```python
profile.to_file("your_report.html")
```
Alternatively, you can obtain the data as json:
```python
# As a string
json_data = profile.to_json()

# As a file
profile.to_file("your_report.json")
```

### Large datasets

Version 2.4 introduces minimal mode. 
This is a default configuration that disables expensive computations (such as correlations and dynamic binning).
Use the following syntax:

```python
profile = ProfileReport(large_dataset, minimal=True)
profile.to_file("output.html")
```

### Command line usage

For standard formatted CSV files that can be read immediately by pandas, you can use the `pandas_profiling` executable. Run

	pandas_profiling -h

for information about options and arguments.

### Advanced usage

A set of options is available in order to adapt the report generated.

* `title` (`str`): Title for the report ('Pandas Profiling Report' by default).
* `pool_size` (`int`): Number of workers in thread pool. When set to zero, it is set to the number of CPUs available (0 by default).
* `progress_bar` (`bool`): If True, `pandas-profiling` will display a progress bar.

More settings can be found in the [default configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_default.yaml), [minimal configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_minimal.yaml) and [dark themed configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_dark.yaml).

__Example__
```python
profile = df.profile_report(title='Pandas Profiling Report', plot={'histogram': {'bins': 8}})
profile.to_file("output.html")
```

# Supporting open source

Maintaining and developing the open-source code for pandas-profiling, with millions of downloads and thousands of users, would not be possible with support of our gracious sponsors.

<table>
<tr>
<td>

<img alt="Lambda Labs" src="https://pandas-profiling.github.io/pandas-profiling/docs/assets/lambda-labs.png" width="500" />

</td>
<td>

[Lambda workstations](https://lambdalabs.com/), servers, laptops, and cloud services power engineers and researchers at Fortune 500 companies and 94% of the top 50 universities. [Lambda Cloud](https://lambdalabs.com/service/gpu-cloud) offers 4 & 8 GPU instances starting at $1.50 / hr. Pre-installed with TensorFlow, PyTorch, Ubuntu, CUDA, and cuDNN.

</td>
</tr>
</table>

We would like to thank our generous Github Sponsors supporters who make pandas-profiling possible: 

    Martin Sotir, Joseph Yuen, Brian Lee, Stephanie Rivera, nscsekhar, abdulAziz

More info if you would like to appear here: [Github Sponsor page](https://github.com/sponsors/sbrugman)


## Types

Types are a powerful abstraction for effective data analysis, that goes beyond the logical data types (integer, float etc.).
`pandas-profiling` currently recognizes the following types: _Boolean, Numerical, Date, Categorical, URL, Path, File_ and _Image_.

We have developed a type system for Python, tailored for data analysis: [visions](https://github.com/dylan-profiler/visions).
Selecting the right typeset drastically reduces the complexity the code of your analysis.
Future versions of `pandas-profiling` will have extended type support through `visions`!

## Contributing

Read on getting involved in the [Contribution Guide](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/pages/contribution_guidelines.html).
A low threshold place to ask questions or start contributing is by reaching out on the pandas-profiling Slack. [Join the Slack community](https://join.slack.com/t/pandas-profiling/shared_invite/zt-hfy3iwp2-qEJSItye5QBZf8YGFMaMnQ).

## Editor integration
### PyCharm integration 
1. Install `pandas-profiling` via the instructions above
2. Locate your `pandas-profiling` executable.

	  On macOS / Linux / BSD:
	
	```console
	$ which pandas_profiling
	(example) /usr/local/bin/pandas_profiling
	```
	
	  On Windows:
	
	```console
	$ where pandas_profiling
	(example) C:\ProgramData\Anaconda3\Scripts\pandas_profiling.exe
	```

2. In Pycharm, go to _Settings_ (or _Preferences_ on macOS) > _Tools_ > _External tools_
3. Click the _+_ icon to add a new external tool
4. Insert the following values
	- Name: Pandas Profiling
    - Program: *__The location obtained in step 2__*
    - Arguments: "$FilePath$" "$FileDir$/$FileNameWithoutAllExtensions$_report.html"
    - Working Directory: $ProjectFileDir$
  
<img alt="PyCharm Integration" src="https://pandas-profiling.github.io/pandas-profiling/docs/assets/pycharm-integration.png" width="400" />
  
To use the PyCharm Integration, right click on any dataset file:
_External Tools_ > _Pandas Profiling_.

### Other integrations

Other editor integrations may be contributed via pull requests.

## Dependencies

The profile report is written in HTML and CSS, which means pandas-profiling requires a modern browser. 

You need [Python 3](https://python3statement.org/) to run this package. Other dependencies can be found in the requirements files:

| Filename | Requirements|
|----------|-------------|
| [requirements.txt](https://github.com/pandas-profiling/pandas-profiling/blob/master/requirements.txt) | Package requirements|
| [requirements-dev.txt](https://github.com/pandas-profiling/pandas-profiling/blob/master/requirements-dev.txt)  |  Requirements for development|
| [requirements-test.txt](https://github.com/pandas-profiling/pandas-profiling/blob/master/requirements-test.txt) | Requirements for testing|
| [setup.py](https://github.com/pandas-profiling/pandas-profiling/blob/master/setup.py) | Requirements for Widgets etc. |
