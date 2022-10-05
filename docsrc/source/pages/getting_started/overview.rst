========
Overview
========

.. image:: https://ydataai.github.io/pandas-profiling/docs/assets/logo_header.png
  :alt: Pandas Profiling Logo Header

.. image:: https://github.com/ydataai/pandas-profiling/actions/workflows/tests.yml/badge.svg?branch=master
  :alt: Build Status
  :target: https://github.com/ydataai/pandas-profiling/actions/workflows/tests.yml

.. image:: https://codecov.io/gh/ydataai/pandas-profiling/branch/master/graph/badge.svg?token=gMptB4YUnF
  :alt: Code Coverage
  :target: https://codecov.io/gh/ydataai/pandas-profiling

.. image:: https://img.shields.io/github/release/pandas-profiling/pandas-profiling.svg
  :alt: Release Version
  :target: https://github.com/ydataai/pandas-profiling/releases

.. image:: https://img.shields.io/pypi/pyversions/pandas-profiling
  :alt: Python Version
  :target: https://pypi.org/project/pandas-profiling/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :alt: Code style: black
  :target: https://github.com/python/black

``pandas-profiling`` generates profile reports from a pandas ``DataFrame``.
The pandas ``df.describe()`` function is handy yet a little basic for exploratory data analysis. ``pandas-profiling`` extends pandas ``DataFrame`` with ``df.profile_report()``,  
which automatically generates a standardized univariate and multivariate report for data understanding. 

For each column, the following information (whenever relevant for the column type) is presented in an interactive HTML report:

* **Type inference**: detect the types of columns in a ``DataFrame``
* **Essentials**: type, unique values, indication of missing values
* **Quantile statistics**: minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics**: mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent and extreme values**
* **Histograms:** categorical and numerical
* **Correlations**: high correlation warnings, based on different correlation metrics (Spearman, Pearson, Kendall, Cramér's V, Phik)
* **Missing values**: through counts, matrix, heatmap and dendrograms
* **Duplicate rows**: list of the most common duplicated rows
* **Text analysis**: most common categories (uppercase, lowercase, separator), scripts (Latin, Cyrillic) and blocks (ASCII, Cyrilic)
* **File and Image analysis**: file sizes, creation dates, dimensions, indication of truncated images and existence of EXIF metadata


The report contains three additional sections: 

* **Overview**: mostly global details about the dataset (number of records, number of variables, overall missigness and duplicates, memory footprint)
* **Alerts**: a comprehensive and automatic list of potential data quality issues (high correlation, skewness, uniformity, zeros, missing values, constant values, between others) 
* **Reproduction**: technical details about the analysis (time, version and configuration)

The package can be used via code but also directly as a CLI utility. The generated interactive report can be consumed and shared as regular HTML or embedded in an interactive way inside Jupyter Notebooks. 

.. NOTE::
   **⚡ Looking for a Spark backend to profile large datasets?**

   While not yet finished, a Spark backend is in development. Progress can be tracked `here <https://github.com/ydataai/pandas-profiling/projects/3>`_. Testing and contributions are welcome!