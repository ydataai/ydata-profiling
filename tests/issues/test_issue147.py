"""
Test for issue 147:
https://github.com/pandas-profiling/pandas-profiling/issues/147
"""
from pathlib import Path

import pandas as pd
import requests

from pandas_profiling import ProfileReport


def test_issue147(tmpdir):
    file_name = Path(str(tmpdir)) / "userdata1.parquet"
    data = requests.get(
        "https://github.com/Teradata/kylo/raw/master/samples/sample-data/parquet/userdata2.parquet"
    )
    file_name.write_bytes(data.content)

    df = pd.read_parquet(str(file_name), engine="pyarrow")
    report = ProfileReport(df, title="PyArrow with Pandas Parquet Backend")
    html = report.to_html()
    assert type(html) == str
    assert "<p class=h2>Dataset info</p>" in html
