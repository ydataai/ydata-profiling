# pandas-profiling

---

⚠️ **`pandas-profiling` package naming was changed. To continue profiling data use [`ydata-profiling`](https://github.com/ydataai/ydata-profiling) instead!** 

This repo implements the brownout strategy for deprecating the pandas-profiling package on PyPI.⚠️

---


<p align="center"><img width="500" src="https://ydata-profiling.ydata.ai/docs/assets/logo_header.png" alt="Pandas Profiling Logo"></p>

### 🎊 New year, new face, more functionalities! 
> Thank you for using and following ``pandas-profiling`` developments. Yet, we have a new exciting feature - we are now thrilled to announce
> that <u>Spark</u> is now part of the Data Profiling family from version 4.0.0 onwards
> 
> With its introduction, there was also the need for a new naming, one that will allow to decouple the concept of profiling from the Pandas Dataframes - `ydata-profiling`! 
> 
> But fear not, `pip install pandas-profiling` will still be a valid for a while, and we will keep investing in growing the best open-source for data profiling, so you can use it for even more use cases.
# How to fix the error for the main use cases

- use `pip install ydata-profiling` rather than `pip install pandas-profiling`
- replace `pandas-profiling` by `ydata-profiling` in your pip requirements files (requirements.txt, setup.py, setup.cfg, Pipfile, etc ...)
- if the `pandas-profiling` package is used by one of your dependencies it would be great if you take some time to track which package uses `pandas_profiling` instead of `ydata_profiling` for the imports

## Schedule for deprecation
- `ydata-profiling` was launched in February 1st. 
- `pip install pandas-profiling` will still be supported until **April 1st**, but a warning will be thrown. `from pandas_profiling import ProfileReport` will be supported until April 1st.
- After April 1st, an error will be thrown if `pip install pandas-profiling` is used. Use `pip install ydata-profiling` instead.
- After April 1st, an error will be thrown if `from pandas_profiling import ProfileReport` is used. Use `from ydata_profiling import ProfileReport` instead.


### About pandas-profiling
`pandas-profiling` primary goal is to provide a one-line Exploratory Data Analysis (EDA) experience in a consistent and fast solution. Like pandas `df.describe()` function, that is so handy, pandas-profiling delivers an extended analysis of a DataFrame while alllowing the data analysis to be exported in different formats such as **html** and **json**.

The package outputs a simple and digested analysis of a dataset, including **time-series** and **text**. 


<p align="center">
  <a href="https://pandas-profiling.ydata.ai/docs/master/">Documentation</a>
  |
  <a href="https://discord.com/invite/mw7xjJ7b7s">Discord</a>
  | 
  <a href="https://stackoverflow.com/questions/tagged/pandas-profiling">Stack Overflow</a>
  |
  <a href="https://pandas-profiling.ydata.ai/docs/master/pages/reference/changelog.html#changelog">Latest changelog</a>

</p>

<p align="center">
  Do you like this project? Show us your love and <a href="https://engage.ydata.ai">give feedback!</a>
</p>
