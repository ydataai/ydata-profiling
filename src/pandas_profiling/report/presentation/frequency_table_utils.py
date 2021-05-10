from typing import Any, Dict, List

import numpy as np
import pandas as pd


def freq_table(freqtable: pd.Series, n: int, max_number_to_print: int) -> List[Dict]:
    """Render the rows for a frequency table (value, count).

    Args:
      freqtable: The frequency table.
      n: The total number of values.
      max_number_to_print: The maximum number of observations to print.

    Returns:
        The rows of the frequency table.
    """

    # TODO: replace '' by '(Empty)' ?

    if max_number_to_print > n:
        max_number_to_print = n

    if max_number_to_print < len(freqtable):
        freq_other = np.sum(freqtable.iloc[max_number_to_print:])
        min_freq = freqtable.values[max_number_to_print]
    else:
        freq_other = 0
        min_freq = 0

    freq_missing = n - np.sum(freqtable)
    # No values
    if len(freqtable) == 0:
        return []

    max_freq = max(freqtable.values[0], freq_other, freq_missing)

    # TODO: Correctly sort missing and other
    # No values
    if max_freq == 0:
        return []

    rows = []
    for label, freq in freqtable.iloc[0:max_number_to_print].items():
        rows.append(
            {
                "label": label,
                "width": freq / max_freq,
                "count": freq,
                "percentage": float(freq) / n,
                "n": n,
                "extra_class": "",
            }
        )

    if freq_other > min_freq:
        other_count = str(freqtable.count() - max_number_to_print)
        rows.append(
            {
                "label": f"Other values ({other_count})",
                "width": freq_other / max_freq,
                "count": freq_other,
                # Hack for tables with combined...
                "percentage": min(float(freq_other) / n, 1.0),
                "n": n,
                "extra_class": "other",
            }
        )

    if freq_missing > min_freq:
        rows.append(
            {
                "label": "(Missing)",
                "width": freq_missing / max_freq,
                "count": freq_missing,
                "percentage": float(freq_missing) / n,
                "n": n,
                "extra_class": "missing",
            }
        )

    return rows


def extreme_obs_table(
    freqtable: pd.Series, number_to_print: int, n: int
) -> List[Dict[str, Any]]:
    """Similar to the frequency table, for extreme observations.

    Args:
      freqtable: The (sorted) frequency table.
      number_to_print: The number of observations to print.
      n: The total number of observations.

    Returns:
        The HTML rendering of the extreme observation table.
    """

    obs_to_print = freqtable.iloc[:number_to_print]
    max_freq = obs_to_print.max()

    rows = [
        {
            "label": label,
            "width": freq / max_freq if max_freq != 0 else 0,
            "count": freq,
            "percentage": float(freq) / n,
            "extra_class": "",
            "n": n,
        }
        for label, freq in obs_to_print.items()
    ]

    return rows
