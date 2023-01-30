"""
    Time-series profiling example for USA AirQuality dataset
"""
import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file
from ydata_profiling.visualisation.plot import timeseries_heatmap

if __name__ == "__main__":

    file_name = cache_file(
        "pollution_us_2000_2016.csv",
        "https://query.data.world/s/mz5ot3l4zrgvldncfgxu34nda45kvb",
    )

    df = pd.read_csv(file_name, index_col=[0])

    # Prepare the dataset
    # We will only consider the data from Arizone state for this example
    df = df[df["State"] == "Arizona"]
    df["Date Local"] = pd.to_datetime(df["Date Local"])

    # Plot the time heatmap distribution for the per entity time-series
    timeseries_heatmap(dataframe=df, entity_column="Site Num", sortby="Date Local")

    # Return the profile per station
    for group in df.groupby("Site Num"):
        # Running 1 profile per station
        profile = ProfileReport(group[1], tsmode=True, sortby="Date Local")

        profile.to_file(f"Ts_Profile_{group[0]}.html")
