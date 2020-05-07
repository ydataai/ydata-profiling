============
Introduction
============

.. image:: https://pandas-profiling.github.io/pandas-profiling/docs/assets/logo_header.png
  :alt: Pandas Profiling Logo Header

.. image:: https://travis-ci.com/pandas-profiling/pandas-profiling.svg?branch=master
  :alt: Build Status
  :target: https://travis-ci.com/pandas-profiling/pandas-profiling)

.. image:: https://codecov.io/gh/pandas-profiling/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF
  :alt: Code Coverage
  :target: https://codecov.io/gh/pandas-profiling/pandas-profiling)

.. image:: https://img.shields.io/github/release/pandas-profiling/pandas-profiling.svg
  :alt: Release Version
  :target: https://github.com/pandas-profiling/pandas-profiling/releases

.. image:: https://img.shields.io/pypi/pyversions/pandas-profiling
  :alt: Python Version
  :target: https://pypi.org/project/pandas-profiling/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style: black
  :target: https://github.com/python/black

Generates profile reports from a pandas ``DataFrame``.
The pandas ``df.describe()`` function is great but a little basic for serious exploratory data analysis.
``pandas_profiling`` extends the pandas DataFrame with ``df.profile_report()`` for quick data analysis.

For each column the following statistics - if relevant for the column type - are presented in an interactive HTML report:

* **Type inference**: detect the types of columns in a dataframe.
* **Essentials**: type, unique values, missing values
* **Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics** like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histograms**
* **Correlations** highlighting of highly correlated variables, Spearman, Pearson and Kendall matrices
* **Missing values** matrix, count, heatmap and dendrogram of missing values
* **Duplicate rows** Lists the most occurring duplicate rows
* **Text analysis** learn about categories (Uppercase, Space), scripts (Latin, Cyrillic) and blocks (ASCII) of text data