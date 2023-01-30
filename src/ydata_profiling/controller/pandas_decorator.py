"""This file add the decorator on the DataFrame object."""
from pandas import DataFrame

from ydata_profiling.profile_report import ProfileReport


def profile_report(df: DataFrame, **kwargs) -> ProfileReport:
    """Profile a DataFrame.

    Args:
        df: The DataFrame to profile.
        **kwargs: Optional arguments for the ProfileReport object.

    Returns:
        A ProfileReport of the DataFrame.
    """
    p = ProfileReport(df, **kwargs)
    return p


DataFrame.profile_report = profile_report
