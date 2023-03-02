import warnings
from dataclasses import asdict
from typing import Any, List, Optional, Tuple, Union

import pandas as pd
from dacite import from_dict
from pandas_profiling.config import Settings
from pandas_profiling.model.description import BaseDescription
from pandas_profiling.profile_report import ProfileReport


def _should_wrap(v1: Any, v2: Any) -> bool:
    if isinstance(v1, (list, dict)):
        return False
    if isinstance(v1, pd.DataFrame) and isinstance(v2, pd.DataFrame):
        return v1.equals(v2)
    if isinstance(v1, pd.Series) and isinstance(v2, pd.Series):
        return v1.equals(v2)
    try:
        return v1 == v2
    except ValueError:
        return False


def _update_merge_dict(d1: Any, d2: Any) -> dict:
    # Unwrap d1 and d2 in new dictionary to keep non-shared keys with **d1, **d2
    # Next unwrap a dict that treats shared keys
    # If two keys have an equal value, we take that value as new value
    # If the values are not equal, we recursively merge them
    return {
        **d1,
        **d2,
        **{
            k: [d1[k], d2[k]]
            if _should_wrap(d1[k], d2[k])
            else _update_merge_mixed(d1[k], d2[k])
            for k in {*d1} & {*d2}
        },
    }


def _update_merge_seq(d1: Any, d2: Any) -> Union[list, tuple]:
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


def _update_merge_mixed(d1: Any, d2: Any) -> Union[dict, list, tuple]:
    if isinstance(d1, dict) and isinstance(d2, dict):
        return _update_merge_dict(d1, d2)
    else:
        return _update_merge_seq(d1, d2)


def _update_merge(d1: Optional[dict], d2: dict) -> dict:
    # For convenience in the loop, allow d1 to be empty initially
    if d1 is None:
        return d2

    if not isinstance(d1, dict) or not isinstance(d2, dict):
        raise TypeError(
            "Both arguments need to be of type dictionary (ProfileReport.description_set)"
        )
    return _update_merge_dict(d1, d2)


def _placeholders(*reports: dict) -> None:
    """Generates placeholders in the dataset descriptions where needed"""
    keys = {v for r in reports for v in r["scatter"]}
    type_keys = {v for r in reports for v in r["table"]["types"]}
    for report in reports:
        # Interactions
        for k1 in keys:
            for k2 in keys:
                if k1 not in report["scatter"]:
                    report["scatter"][k1] = {}
                if k2 not in report["scatter"][k1]:
                    report["scatter"][k1][k2] = ""
        # Types
        for type_key in type_keys:
            if type_key not in report["table"]["types"]:
                report["table"]["types"][type_key] = 0


def _update_titles(reports: List[ProfileReport]) -> None:
    """Redefine title of reports with the default one."""
    for idx, report in enumerate(reports):
        if report.config.title == "Pandas Profiling Report":
            report.config.title = f"Dataset {chr(65 + idx)}"


def _compare_title(titles: List[str]) -> str:
    if all(titles[0] == title for title in titles[1:]):
        return titles[0]
    else:
        title = ", ".join(titles[:-1])
        return f"<em>Comparing</em> {title} <em>and</em> {titles[-1]}"


def _compare_profile_report_preprocess(
    reports: List[ProfileReport],
) -> Tuple[List[str], List[dict]]:
    # Use titles as labels
    labels = [report.config.title for report in reports]

    # Use color per report if not custom set
    if len(reports[0].config.html.style.primary_colors) > 1:
        for idx, report in enumerate(reports):
            report.config.html.style.primary_colors = [
                report.config.html.style.primary_colors[idx]
            ]
    # Obtain description sets
    descriptions = [asdict(report.get_description()) for report in reports]
    for label, description in zip(labels, descriptions):
        description["analysis"]["title"] = label

    return labels, descriptions


def _compare_dataset_description_preprocess(
    reports: List[dict],
) -> Tuple[List[str], List[dict]]:
    labels = [report["analysis"]["title"] for report in reports]
    return labels, reports


def compare(
    reports: List[ProfileReport],
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
    if len(reports) > 2:
        warnings.warn(
            "Comparison of more than two reports is not supported. "
            "Reports may be produced, but may yield unexpected formatting."
        )
    report_types = [r.config.vars.timeseries.active for r in reports]
    if all(report_types) != any(report_types):
        raise ValueError(
            "Comparison between timeseries and tabular reports is not supported"
        )
    is_df_available = [r.df is not None for r in reports]
    if not all(is_df_available):
        raise ValueError("Reports where not initialized with a DataFrame.")
    features = [set(r.df.columns) for r in reports]  # type: ignore
    if not all(features[0] == x for x in features):
        warnings.warn(
            "The datasets being profiled have a different set of columns. "
            "Only the left side profile will be calculated."
        )
    base_features = reports[0].df.columns  # type: ignore
    for report in reports[1:]:
        cols_2_compare = [col for col in base_features if col in report.df.columns]  # type: ignore
        report.df = report.df.loc[:, cols_2_compare]  # type: ignore
    reports = [r for r in reports if not r.df.empty]  # type: ignore
    if len(reports) == 1:
        return reports[0]
    if config is None:
        config = Settings()
    if all(isinstance(report, ProfileReport) for report in reports):
        # Type ignore is needed as mypy does not pick up on the type narrowing
        # Consider using TypeGuard (3.10): https://docs.python.org/3/library/typing.html#typing.TypeGuard
        _update_titles(reports)
        labels, descriptions = _compare_profile_report_preprocess(reports)  # type: ignore
    elif all(isinstance(report, dict) for report in reports):
        labels, descriptions = _compare_dataset_description_preprocess(reports)  # type: ignore
    else:
        raise TypeError("")
    config.html.style._labels = labels
    _placeholders(*descriptions)
    res: dict = _update_merge(None, descriptions[0])
    for r in descriptions[1:]:
        res = _update_merge(res, r)
    res["analysis"]["title"] = _compare_title(res["analysis"]["title"])
    profile = ProfileReport(None, config=config)
    profile._description_set = from_dict(data_class=BaseDescription, data=res)
    return profile
