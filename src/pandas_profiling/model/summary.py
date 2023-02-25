"""Compute statistical description of datasets."""

from typing import Any, Dict, Optional

from multimethod import multimethod
from pandas_profiling.config import Settings
from pandas_profiling.model.description_target import TargetDescription
from pandas_profiling.model.summarizer import BaseSummarizer
from tqdm import tqdm
from visions import VisionsTypeset


@multimethod
def describe_1d(
    config: Settings,
    series: Any,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    target_description: Optional[TargetDescription],
) -> Dict[str, Any]:
    """Describe one data column.

    Parameters
    ----------
    config : Settings
        User configuration.
    series : Any
        One column of data.
    summarizer : BaseSummarizer
        Summarizer with switch for all types of column.
    typeset: VisionsTypeset
        Data type inferrer.
    target_description : Optional[TargetDescription]
        Description of target column, if target defined. None if not.

    Returns
    -------
    Dict[str, Any]
        Description dictionary of series from parameters.
    """
    raise NotImplementedError()


@multimethod
def get_series_descriptions(
    config: Settings,
    df: Any,
    summarizer: BaseSummarizer,
    typeset: VisionsTypeset,
    pbar: tqdm,
    target_description: Optional[TargetDescription],
) -> Dict[str, Any]:
    """Create description for all columns.

    Parameters
    ----------
    config : Settings
        User configuration.
    df : Any
        Data
    summarizer : BaseSummarizer
        Summarizer with switch for all types of column.
    typeset : VisionsTypeset
        Data type inferrer.
    pbar : tqdm

    target_description: Optional[TargetDescription]
        Description of target column, if target defined. None if not.
    """
    raise NotImplementedError()
