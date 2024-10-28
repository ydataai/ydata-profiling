"""
Test for issue 147:
https://github.com/ydataai/ydata-profiling/issues/147
"""
import pandas as pd

from ydata_profiling import ProfileReport


def test_issue147(get_data_file):
    file_name = get_data_file(
        "userdata1.parquet",
        "https://github.com/Teradata/kylo/raw/master/samples/sample-data/parquet/userdata2.parquet",
    )

    df = pd.read_parquet(str(file_name), engine="pyarrow")
    report = ProfileReport(
        df, title="PyArrow with Pandas Parquet Backend", progress_bar=False, pool_size=1
    )
    html = report.to_html()
    assert type(html) == str
    assert "Dataset statistics</p>" in html
