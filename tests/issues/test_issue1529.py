"""
Test for issue 1529:
https://github.com/ydataai/ydata-profiling/issues/1529
"""
import json

import pandas as pd

from ydata_profiling import ProfileReport


def test_issue1529():
    previous_dataset = pd.DataFrame(
        data=[(1000, 42), (900, 30), (1500, 40), (1800, 38)],
        columns=["rent_per_month", "total_area"],
    )
    current_dataset = pd.DataFrame(
        data=[(5000, 350), (9000, 600), (5000, 400), (3500, 500), (6000, 600)],
        columns=["rent_per_month", "total_area"],
    )
    previous_dataset_report = ProfileReport(
        previous_dataset, title="Previous dataset report"
    )
    current_dataset_report = ProfileReport(
        current_dataset, title="Current dataset report"
    )
    comparison_report = previous_dataset_report.compare(current_dataset_report)
    json_str = comparison_report.to_json()
    compare_dict = json.loads(json_str)
    assert compare_dict is not None and len(compare_dict) > 0
    assert (
        compare_dict["analysis"]["title"]
        == "<em>Comparing</em> Previous dataset report <em>and</em> Current dataset report"
    )
