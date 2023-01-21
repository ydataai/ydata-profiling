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

``pandas-profiling`` primary goal is to provide a one-line Exploratory Data Analysis (EDA) experience in a consistent and fast solution. Like pandas `df.describe()` function, that is so handy, pandas-profiling delivers an extended analysis of a DataFrame while alllowing the data analysis to be exported in different formats such as **html** and **json**.

The package outputs a simple and digested analysis of a dataset, including **time-series** and **text**.

Key features
------------
- **Type inference**: automatic detection of columns' data types (*Categorical*, *Numerical*, *Date*, etc.)
- **Warnings**: A summary of the problems/challenges in the data that you might need to work on (*missing data*, *inaccuracies*, *skewness*, etc.)
- **Univariate analysis**: including descriptive statistics (mean, median, mode, etc) and informative visualizations such as distribution histograms
- **Multivariate analysis**: including correlations, a detailed analysis of missing data, duplicate rows, and visual support for variables pairwise interaction
- **Time-Series**: including different statistical information relative to time dependent data such as auto-correlation and seasonality, along ACF and PACF plots.
- **Text analysis**: most common categories (uppercase, lowercase, separator), scripts (Latin, Cyrillic) and blocks (ASCII, Cyrilic)
- **File and Image analysis**: file sizes, creation dates, dimensions, indication of truncated images and existence of EXIF metadata
- **Compare datasets**: one-line solution to enable a fast and complete report on the comparison of datasets
- **Flexible output formats**: all analysis can be exported to an HTML report that can be easily shared with different parties, as JSON for an easy integration in automated systems and as a widget in a Jupyter Notebook.

The report contains three additional sections: 

* **Overview**: mostly global details about the dataset (number of records, number of variables, overall missigness and duplicates, memory footprint)
* **Alerts**: a comprehensive and automatic list of potential data quality issues (high correlation, imbalance, skewness, uniformity, zeros, missing values, constant values, between others) 
* **Reproduction**: technical details about the analysis (time, version and configuration)

The package can be used via code but also directly as a CLI utility. The generated interactive report can be consumed and shared as regular HTML or embedded in an interactive way inside Jupyter Notebooks. 


.. NOTE::
   **🎁 Latest features**
    - Looking for how you can do an EDA for Time-Series 🕛 ? Check `this blogpost <https://towardsdatascience.com/how-to-do-an-eda-for-time-series-cbb92b3b1913>`_
    - You want to compare 2 datasets and get a report? Check `this blogpost <https://medium.com/towards-artificial-intelligence/how-to-compare-2-dataset-with-pandas-profiling-2ae3a9d7695e>`_