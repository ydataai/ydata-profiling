from pathlib import Path

import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.cache import cache_file

if __name__ == "__main__":
    file_name = cache_file("auto2.dta", "http://www.stata-press.com/data/r15/auto2.dta")
    df = pd.read_stata(file_name)

    # In case that a sample of the real data (cars) would disclose sensitive information, we can replace it with
    # mock data. For illustrative purposes, we use data based on cars from a popular game series.
    mock_data = pd.DataFrame(
        {
            "make": ["Blista Kanjo", "Sentinel", "Burrito"],
            "price": [58000, 95000, 65000],
            "mpg": [20, 30, 22],
            "rep78": ["Average", "Excellent", "Fair"],
            "headroom": [2.5, 3.0, 1.5],
            "trunk": [8, 10, 4],
            "weight": [1050, 1600, 2500],
            "length": [165, 170, 180],
            "turn": [40, 50, 32],
            "displacement": [80, 100, 60],
            "gear_ratio": [2.74, 3.51, 2.41],
            "foreign": ["Domestic", "Domestic", "Foreign"],
        }
    )

    report = ProfileReport(
        df.sample(frac=0.25),
        title="Masked data",
        dataset={
            "description": "This profiling report was generated using a sample of 5% of the original dataset.",
            "copyright_holder": "StataCorp LLC",
            "copyright_year": "2020",
            "url": "http://www.stata-press.com/data/r15/auto2.dta",
        },
        sensitive=True,
        sample={
            "name": "Mock data sample",
            "data": mock_data,
            "caption": "Disclaimer: this is synthetic data generated based on the format of the data in this table.",
        },
        vars={"cat": {"words": True, "characters": True}},
        interactions=None,
    )
    report.to_file(Path("masked_report.html"))
