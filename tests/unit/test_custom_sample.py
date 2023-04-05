import pandas as pd

from ydata_profiling import ProfileReport
from ydata_profiling.utils.dataframe import hash_dataframe


def test_custom_sample():
    df = pd.DataFrame({"test": [1, 2, 3, 4, 5]})

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

    # Length left out due to correlation with weight.
    report = ProfileReport(
        df,
        title="Test custom sample",
        sample={
            "name": "Mock data sample",
            "data": mock_data,
            "caption": "Disclaimer: this is synthetic data generated based on the format of the data in this table.",
        },
        minimal=True,
    )

    samples = report.get_description().sample
    assert len(samples) == 1
    sample = samples[0]
    assert sample.id == "custom"
    assert hash_dataframe(sample.data) == hash_dataframe(mock_data)
    assert sample.name == "Mock data sample"
    assert (
        sample.caption
        == "Disclaimer: this is synthetic data generated based on the format of the data in this table."
    )

    html = report.to_html()
    assert "Mock data sample" in html
    assert all(make in html for make in mock_data["make"].values.tolist())
    assert (
        "Disclaimer: this is synthetic data generated based on the format of the data in this table"
        in html
    )
