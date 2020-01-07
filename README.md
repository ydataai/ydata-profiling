# Pandas Profiling
[![Build Status](https://travis-ci.com/pandas-profiling/pandas-profiling.svg?branch=master)](https://travis-ci.com/pandas-profiling/pandas-profiling)
[![Code Coverage](https://codecov.io/gh/pandas-profiling/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF)](https://codecov.io/gh/pandas-profiling/pandas-profiling)
[![Release Version](https://img.shields.io/github/release/pandas-profiling/pandas-profiling.svg)](https://github.com/pandas-profiling/pandas-profiling/releases)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/pandas-profiling/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

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

## Announcements

With your help, we got approved for [GitHub Sponsors](https://github.com/sponsors/sbrugman)! 
It's extra exciting that GitHub **matches your contribution** for the first year.
Therefore, we welcome you to support the project through GitHub! 

The v2.4 release includes many new features (performance, exporting, GUI and datasets) and stability improvements.

 - [Sponsor the project on GitHub](https://github.com/sponsors/sbrugman)
 - [Read the release notes v2.4](https://github.com/pandas-profiling/pandas-profiling/releases/tag/v2.4.0) 

 *January 7, 2020*

---

_Contents:_ **[Examples](#examples)** |
**[Installation](#installation)** | **[Documentation](#documentation)** |
**[Large datasets](#large-datasets)** | **[Command line usage](#command-line-usage)** |
**[Advanced usage](#advanced-usage)** |
**[Types](#types)** | **[How to contribute](#how-to-contribute)** |
**[Editor Integration](#editor-integration)** | **[Dependencies](#dependencies)**

---

## Examples

The following examples can give you an impression of what the package can do:

* [Census Income](http://pandas-profiling.github.io/pandas-profiling/examples/census/census_report.html) (US Adult Census data relating income)
* [NASA Meteorites](http://pandas-profiling.github.io/pandas-profiling/examples/meteorites/meteorites_report.html) (comprehensive set of meteorite landings)
* [Titanic](http://pandas-profiling.github.io/pandas-profiling/examples/titanic/titanic_report.html) (the "Wonderwall" of datasets)
* [NZA](http://pandas-profiling.github.io/pandas-profiling/examples/nza/nza_report.html) (open data from the Dutch Healthcare Authority)
* [Stata Auto](http://pandas-profiling.github.io/pandas-profiling/examples/stata_auto/stata_auto_report.html) (1978 Automobile data)
* [Vektis](http://pandas-profiling.github.io/pandas-profiling/examples/vektis/vektis_report.html) (Vektis Dutch Healthcare data)
* [Website Inaccessibility](http://pandas-profiling.github.io/pandas-profiling/examples/website_inaccessibility/website_inaccessibility_report.html) (demonstrates the URL type)
* [Colors](http://pandas-profiling.github.io/pandas-profiling/examples/colors/colors_report.html) (a simple colors dataset)

## Installation

### Using pip

[![PyPi Downloads](https://pepy.tech/badge/pandas-profiling)](https://pepy.tech/project/pandas-profiling)
[![PyPi Monthly Downloads](https://pepy.tech/badge/pandas-profiling/month)](https://pepy.tech/project/pandas-profiling/month)
[![PyPi Version](https://badge.fury.io/py/pandas-profiling.svg)](https://pypi.org/project/pandas-profiling/)

You can install using the pip package manager by running

    pip install pandas-profiling
    
Alternatively, you could install directly from Github:

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

The documentation for `pandas_profiling` can be found [here](https://pandas-profiling.github.io/pandas-profiling/docs/).

### Getting started

Start by loading in your pandas DataFrame, e.g. by using
```python
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.DataFrame(
    np.random.rand(100, 5),
    columns=['a', 'b', 'c', 'd', 'e']
)
```
To generate the report, run:
```python
profile = ProfileReport(df, title='Pandas Profiling Report', style={'full_width':True})
```

#### Jupyter Notebook

We recommend generating reports interactively by using the Jupyter notebook. 
There are two interfaces (see animations below): through widgets and through a HTML report.

<img alt="Notebook Widgets" src="http://pandas-profiling.github.io/pandas-profiling/docs/assets/widgets.gif" width="800" />

This is achieved by simply displaying the report. In the Jupyter Notebook, run:
```python
profile
```

The HTML report can be included in a Juyter notebook:

<img alt="HTML" src="http://pandas-profiling.github.io/pandas-profiling/docs/assets/iframe.gif" width="800" />

Run the following code:

```python
profile.to_notebook_iframe()
```

#### Saving the report

If you want to generate a HTML report file, save the `ProfileReport` to an object and use the `to_file()` function:
```python
profile.to_file(output_file="your_report.html")
```
Alternatively, you can obtain the data as json:
```python
# As a string
json_data = profile.to_json()

# As a file
profile.to_file(output_file="your_report.json")
```

### Large datasets

Version 2.4 introduces minimal mode. 
This is a default configuration that disables expensive computations (such as correlations and dynamic binning).
Use the following syntax:

```python
profile = ProfileReport(large_dataset, minimal=True)
profile.to_file(output_file="output.html")
```

### Command line usage

For standard formatted CSV files that can be read immediately by pandas, you can use the `pandas_profiling` executable. Run

	pandas_profiling -h

for information about options and arguments.

### Advanced usage

A set of options is available in order to adapt the report generated.

* `title` (`str`): Title for the report ('Pandas Profiling Report' by default).
* `pool_size` (`int`): Number of workers in thread pool. When set to zero, it is set to the number of CPUs available (0 by default).

More settings can be found in the [default configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_default.yaml), [minimal configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_minimal.yaml) and [dark themed configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_dark.yaml).

__Example__
```python
profile = df.profile_report(title='Pandas Profiling Report', plot={'histogram': {'bins': 8}})
profile.to_file(output_file="output.html")
```

## Types

Types are a powerful abstraction for effective data analysis, that goes beyond the logical data types (integer, float etc.).
`pandas-profiling` currently recognizes the following types:

- Boolean
- Numerical
- Date
- Categorical
- URL
- Path

We have developed a type system for Python, tailored for data analysis: [visions](https://github.com/dylan-profiler/visions).
Selecting the right typeset drastically reduces the complexity the code of your analysis.
Future versions of `pandas-profiling` will have extended type support through `visions`!

## How to contribute

[![Questions: Stackoverflow "pandas-profiling"](https://img.shields.io/badge/stackoverflow%20tag-pandas%20profiling-yellow)](https://stackoverflow.com/questions/tagged/pandas-profiling)

The package is actively maintained and developed as open-source software. 
If `pandas-profiling` was helpful or interesting to you, you might want to get involved. 
There are several ways of contributing and helping our thousands of users.
If you would like to be a industry partner or sponsor, please [drop us a line](mailto:pandasprofiling@gmail.com).

The documentation is generated using [`pdoc3`](https://github.com/pdoc3/pdoc). 
If you are contributing to this project, you can rebuild the documentation using:
```
make docs
```
or on Windows:
```
make.bat docs
```

Read more on getting involved in the [Contribution Guide](https://github.com/pandas-profiling/pandas-profiling/blob/master/CONTRIBUTING.md).


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
  
<img alt="PyCharm Integration" src="http://pandas-profiling.github.io/pandas-profiling/docs/assets/pycharm-integration.png" width="400" />
  
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
