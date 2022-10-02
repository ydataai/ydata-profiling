import warnings
from typing import Any, Dict, List, Optional, Sequence, Union

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.profile_report import ProfileReport


def _isequal(v1: Any, v2: Any) -> bool:
    if isinstance(v1, pd.DataFrame) and isinstance(v2, pd.DataFrame):
        return v1.equals(v2)
    if isinstance(v1, pd.Series) and isinstance(v2, pd.Series):
        return v1.equals(v2)
    if isinstance(v1, dict):
        return False
    if isinstance(v1, list):
        return False

    try:
        return v1 == v2
    except ValueError:
        return False


def _update_merge(d1: Any, d2: Any) -> Union[dict, list, tuple]:
    if d1 is None:
        return d2
    if isinstance(d1, dict) and isinstance(d2, dict):
        # Unwrap d1 and d2 in new dictionary to keep non-shared keys with **d1, **d2
        # Next unwrap a dict that treats shared keys
        # If two keys have an equal value, we take that value as new value
        # If the values are not equal, we recursively merge them

        return {
            **d1,
            **d2,
            **{
                k: [d1[k], d2[k]]
                if _isequal(d1[k], d2[k])
                else _update_merge(d1[k], d2[k])
                for k in {*d1} & {*d2}
            },
        }
    else:
        # This case happens when values are merged
        # It bundle values in a list, making sure
        # to flatten them if they are already lists

        if isinstance(d1, list) and isinstance(d2, list):
            # This is the tuple for alerts
            return d1, d2
        elif isinstance(d1, tuple) and isinstance(d2, list):
            return (*d1, d2)
        else:
            return [
                *(d1 if isinstance(d1, list) else [d1]),
                *(d2 if isinstance(d2, list) else [d2]),
            ]


def _placeholders(*reports) -> List[ProfileReport]:
    """Needed for merging interactions"""
    keys = {v for r in reports for v in r["scatter"].keys()}
    type_keys = {v for r in reports for v in r["table"]["types"].keys()}
    for idx in range(len(reports)):
        # Interactions
        for k1 in keys:
            for k2 in keys:
                if k1 not in reports[idx]["scatter"]:
                    reports[idx]["scatter"][k1] = {}
                if k2 not in reports[idx]["scatter"][k1]:
                    reports[idx]["scatter"][k1][k2] = ""

        # Types
        for type_key in type_keys:
            if type_key not in reports[idx]["table"]["types"]:
                reports[idx]["table"]["types"][type_key] = 0

    return list(reports)


def _compare_title(titles: List[str]) -> str:
    if all(titles[0] == title for title in titles[1:]):
        return titles[0]
    else:
        title = ", ".join(titles[:-1])
        return f"<em>Comparing</em> {title} <em>and</em> {titles[-1]}"


def compare(
    reports: Sequence[Union[ProfileReport, Dict]],
    config: Optional[Settings] = None,
) -> ProfileReport:
    """
    Compare Profile reports

    Args:
        reports: two reports to compare
                 input may either be a ProfileReport, or the summary obtained from report.get_description()
        config: the settings object for the merged ProfileReport

    """
    if len(reports) < 2:
        raise ValueError("At least two reports are required for this comparison")

    if config is None:
        config = Settings()

    if len(reports) > 2:
        warnings.warn(
            "Comparison of more than two reports is in beta. "
            "Reports will be produced, but may yield unexpected formatting."
        )

    if any(not isinstance(report, dict) for report in reports):
        # Use titles as labels
        labels = [report.config.title for report in reports]  # type: ignore

        # Use color per report if not custom set
        if len(reports[0].config.html.style.primary_colors) > 1:  # type: ignore
            for idx, report in enumerate(reports):
                report.config.html.style.primary_colors = [  # type: ignore
                    report.config.html.style.primary_colors[idx]  # type: ignore
                ]

        # Obtain description sets
        reports = [report.get_description() for report in reports]  # type: ignore
    else:
        labels = [report["analysis"]["title"] for report in reports]  # type: ignore

    config.html.style._labels = labels

    reports = _placeholders(*reports)

    res: Optional[dict] = None
    for r in reports:
        res: dict = _update_merge(res, r)  # type: ignore

    res["analysis"]["title"] = _compare_title(res["analysis"]["title"])  # type: ignore

    profile = ProfileReport(None, config=config)
    profile._description_set = res
    return profile
