#pandas-profiling
Generates profile reports from a pandas DataFrame. The *df.describe()* function is great but a little basic for serious exploratory data analysis.

For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:

* **Essentials**:  type, unique values, missing values
* **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histogram**


## Demo

[Click here](http://nbviewer.ipython.org/github/JosPolfliet/pandas-profiling/blob/master/examples/meteorites.ipynb) to see a live demo.


## Installation
### Using pip
You can install using the pip package manager by running

    pip install pandas-profiling

### Using conda
You can install using the conda package manager by running

    conda install -c jos_pol pandas-profiling

I haven't found yet if it is possible to upload it to the main repo (to just be able to type 'conda install pandas-profiling'). Please give me a ping if you have done this.

### From source
Download the source code by cloning the repo or by pressing 'Download ZIP' on this page. Install by navigating to the proper directory and running

    python setup.py install

## Usage
The profile report is written in HTML5 and CSS3, which means pandas-profiling requires a modern browser.

### Jupyter Notebook (formerly IPython)
We recommend generating reports interactively by using the Jupyter notebook.

Start by loading in your pandas DataFrame, e.g. by using

	import pandas as pd

	df=pd.read_csv("/myfilepath/myfile.csv", parse_dates=True, encoding='UTF-8')

To display the report in a Jupyter notebook, run:

	pandas_profiling.ProfileReport(df)

To retrieve the list of variables which are rejected due to high correlation:

    profile = pandas_profiling.ProfileReport(df)
    rejected_variables = profile.get_rejected_variables(threshold=0.9)

If you want to generate a HTML report file, save the ProfileReport to an object and use the *to_file()* function:

    profile = pandas_profiling.ProfileReport(df)
    profile.to_file(outputfile="/tmp/myoutputfile.html")

### Python
For standard formatted CSV files that can be read immediately by pandas, you can use the **profile_csv.py** script. Run

	python profile_csv.py -h

for information about options and arguments.

## Dependencies

* **An internet connection.** Pandas-profiling requires an internet connection to download the Bootstrap and JQuery libraries. I might change this in the future, let me know if you want that sooner than later.
* python (>= 2.7)
* pandas (>=0.19)
* matplotlib  (>=1.4)
* six (>=1.9)

### Key differences between SQL backends

The SQL backend implementation was originally intention to work with HP's Vertica database engine.
For testing purposes, Python's sqlite module is used.
There are some differences that have necessitated a (mostly unnecessary) generality to the code:

- SQLite does not support "schemas": schema is optional on all functions and in the templates.
- SQLite does not support "analytic" functions, such as AVG, PARTITION_BY, etc: these computations are avoided by the analytic option in the templates.
- SQLite names the column from `select count(*) ...` as `count(*)`: these statements are changed to `select count(*) as count, ...`.
- The variable type as stored in the database is unclear in SQLite: the `infer_datatype()` function wraps this code in a `try` clause.


### Variable types

We recognize the pure types of variables as:

- Constant.
- Unique.
- Date.
- Categorical (nominal).
- Ordinal.
- Numeric.
- Binary.
- Other.

Constant and unique can have computer encoding (float, string, integer, date),
but are characterized simply by their distribution.
Similarly, binary and "other" variable types can have many software encodings,
where binary have two distinct values of any encoding and "other" variables are non-numeric with more than 500 distinct values.
Dates are any type of date, and this is relatively straightforward.
Ordinal, categorical, and "other" are similar: they are all categorical types, where the "other" have more than 500 values and the ordinal have a natural ordering.
Finally, numeric variables are perhaps the most simple: any type of number (we make no distinction between ratio and interval).
