==================
Time-Series data
==================

``pandas-profiling`` can be used for a quick Exploratory Data Analysis on time-series data. This is useful for a quick understading on the behaviour of time dependent variables regarding behaviours such as time plots, seasonality, trends and stationarity.

Combined with the profiling reports compare, you're able to compare the evolution and data behaviour through time, in terms of time-series specific statistics such as PACF and ACF plots.

The following syntax can be used to generate a profile under the assumption that the dataset includes time dependent features:

.. code-block:: python

    import pandas as pd

    from ydata_profiling.utils.cache import cache_file
    from ydata_profiling import ProfileReport

    file_name = cache_file(
        "pollution_us_2000_2016.csv",
        "https://query.data.world/s/mz5ot3l4zrgvldncfgxu34nda45kvb",
    )

    df = pd.read_csv(file_name, index_col=[0])

    #Filtering time-series to profile a single site
    site =  df[df['Site Num']==3003]

    profile = ProfileReport(df, tsmode=True, sortby="Date Local", title="Time-Series EDA")

    profile.to_file("report_timeseries.html")

To enable a time-series report to be generated ``ts_mode`` needs to be set to "True". If "True" the variables that have temporal dependence will be automatically identified based on the presence of autocorrelation.
The time-series report uses the ``sortby`` attribute to order the dataset. If not provided it is assumed that the dataset is already ordered.

Customizing time-series variables
------------------------------

In some cases you might be already aware of what variables are expected to be time-series or, perhaps, you just want to ensure that the variables that you want to analyze as time-series are profiled as such:

.. code-block:: python

    import pandas as pd

    from ydata_profiling.utils.cache import cache_file
    from ydata_profiling import ProfileReport

    file_name = cache_file(
        "pollution_us_2000_2016.csv",
        "https://query.data.world/s/mz5ot3l4zrgvldncfgxu34nda45kvb",
    )

    df = pd.read_csv(file_name, index_col=[0])

    #Filtering time-series to profile a single site
    site =  df[df['Site Num']==3003]

    #Setting what variables are time series
    type_schema={
        "NO2 Mean": "timeseries",
        "NO2 1st Max Value": "timeseries",
        'NO2 1st Max Hour': "timeseries",
        "NO2 AQI": "timeseries",
        "cos": "numeric",
        "cat": "numeric",
    }

    profile = ProfileReport(df,
                            tsmode=True,
                            type_schema=type_schema,
                            sortby="Date Local",
                            title="Time-Series EDA for site 3003")

    profile.to_file("report_timeseries.html")

