==================
Time-Series data
==================

``pandas-profiling`` can be used for a quick Exploratory Data Analysis on time-series data. This is useful for a quick understading on the behaviour of time dependent variables regarding behaviours such as time plots, seasonality, trends and stationarity.

Combined with the profiling reports compare, you're able to compare the evolution and data behaviour through time, in terms of time-series specific statistics such as PACF and ACF plots.

The following syntax can be used to generate a profile under the assumption that the dataset includes time dependent features:

.. code-block:: python

    from pandas_profiling import ProfileReport

    df = pd.read_csv("ts_data.csv")
    profile = ProfileReport(df, tsmode=True, sortby="Date", title="Time-Series EDA")

    profile.to_file("report_timeseries.html")


To enable a time-series report to be generated ``ts_mode`` needs to be set to "True". If "True" the variables that have temporal dependence will be automatically identified based on the presence of autocorrelation.
The time-series report uses the ``sortby`` attribute to order the dataset. If not provided it is assumed that the dataset is already ordered.