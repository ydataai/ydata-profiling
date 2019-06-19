# Pandas Profiling
[![Build Status](https://travis-ci.com/pandas-profiling/pandas-profiling.svg)](https://travis-ci.com/pandas-profiling/pandas-profiling)
[![Code Coverage](https://codecov.io/gh/pandas-profiling/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF)](https://codecov.io/gh/pandas-profiling/pandas-profiling)
[![Release Version](https://img.shields.io/github/release/pandas-profiling/pandas-profiling.svg)](https://github.com/pandas-profiling/pandas-profiling/releases)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Generates profile reports from a pandas `DataFrame`. 
The pandas `df.describe()` function is great but a little basic for serious exploratory data analysis. 
`pandas_profiling` extends the pandas DataFrame with `df.profile_report()` for quick data analysis.

For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:

* **Essentials**: type, unique values, missing values
* **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histogram**
* **Correlations** highlighting of highly correlated variables, Spearman, Pearson and Kendall matrices
* **Missing values** matrix, count, heatmap and dendrogram of missing values

## Examples

The following examples can give you an impression of what the package can do:
- [NASA Meteorites](http://pandas-profiling.github.io/pandas-profiling/examples/meteorites/meteorites_report.html)
- [Titanic](http://pandas-profiling.github.io/pandas-profiling/examples/titanic/titanic_report.html)
- [NZA](http://pandas-profiling.github.io/pandas-profiling/examples/nza/nza_report.html)

## Installation

### Using pip

You can install using the pip package manager by running

    pip install pandas-profiling
    
### Using conda

You can install using the conda package manager by running

    conda install -c anaconda pandas-profiling

### From source

Download the source code by cloning the repository or by pressing ['Download ZIP'](https://github.com/pandas-profiling/pandas-profiling/archive/master.zip) on this page. 
Install by navigating to the proper directory and running

    python setup.py install

## Usage

The profile report is written in HTML5 and CSS3, which means pandas-profiling requires a modern browser. 

## Documentation

The documentation for `pandas_profiling` can be found [here](https://pandas-profiling.github.io/pandas-profiling/docs/).
The documentaion is generated using [`pdoc3`](https://github.com/pdoc3/pdoc). 
If you are contribution to this project, you can rebuild the documentation using:
```
make docs
```
or on Windows:
```
make.bat docs
```

### Jupyter Notebook

We recommend generating reports interactively by using the Jupyter notebook. 

Start by loading in your pandas DataFrame, e.g. by using
```python
import numpy as np
import pandas as pd
import pandas_profiling

df = pd.DataFrame(
    np.random.rand(100, 5),
    columns=['a', 'b', 'c', 'd', 'e']
)
```
To display the report in a Jupyter notebook, run:
```python
df.profile_report()
```
To retrieve the list of variables which are rejected due to high correlation:
```python
profile = df.profile_report()
rejected_variables = profile.get_rejected_variables(threshold=0.9)
```
If you want to generate a HTML report file, save the `ProfileReport` to an object and use the `to_file()` function:
```python
profile = df.profile_report(title='Pandas Profiling Report')
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
* `minify_html` (`boolean`): Whether to minify the output HTML.

More settings can be found in the [default configuration file](https://github.com/pandas-profiling/pandas-profiling/blob/master/pandas_profiling/config_default.yaml).

__Example__
```python
profile = df.profile_report(title='Pandas Profiling Report', plot={'histogram': {'bins': 8}})
profile.to_file(output_file="output.html")
```

## Dependencies

* **An internet connection.** Pandas-profiling requires an internet connection to download the Bootstrap and JQuery libraries. I might change this in the future, let me know if you want that sooner than later.
* python ([>= 3.5](https://python3statement.org/))
* pandas (>=0.19)
* matplotlib  (>=1.4)
* missingno
* confuse
* requests
* jinja2
* numpy
* htmlmin (optional)
* phik (optional)

For development and testing we use additional packages which you can find in the [requirements-dev.txt](https://github.com/pandas-profiling/pandas-profiling/blob/master/requirements-dev.txt) and [requirements-test.txt](https://github.com/pandas-profiling/pandas-profiling/blob/master/requirements-test.txt).
