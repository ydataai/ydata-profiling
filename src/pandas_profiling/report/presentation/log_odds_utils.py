from typing import Any, Dict, List

import pandas as pd
from pandas_profiling.model.description_variable import TextDescriptionSupervised


def _limit_count_log_odds_table(
    data: pd.DataFrame, number_to_print: int
) -> pd.DataFrame:
    """Limit count of log odds table rows.
    Get first n/2 and last n/2
    """
    if data.shape[0] < number_to_print:
        return data

    x = data[: number_to_print // 2]
    y = pd.DataFrame([["..."] * data.shape[1]], columns=data.columns, index=["..."])
    z = data[-number_to_print // 2 :]
    return pd.concat([x, y, z])


def log_odds_table(
    description: TextDescriptionSupervised, number_to_print: int
) -> List[Dict[str, Any]]:
    """Render the rows for log odds dataframe with these columns:
        value
        positive_count
        negative_count
        log_odds_ratio


    Args:
      description (TextDescriptionSupervised): Data description with log odds.
      max_number_to_print: The maximum number of observations to print.

    Returns:
        The rows of the log odds table.
    """

    data = _limit_count_log_odds_table(description.log_odds, number_to_print)
    max_val = description.log_odds[description.log_odds_col_name].max()
    min_va = description.log_odds[description.log_odds_col_name].min()
    max_val = max(abs(max_val), abs(min_va))

    ret = []
    for index, row in data.iterrows():
        row_log_odds_ratio = row[description.log_odds_col_name]

        row_dict = {}
        row_dict["label"] = index
        row_dict["positive_count"] = row[description.p_target_value]
        row_dict["negative_count"] = row[description.n_target_value]
        row_dict["log_odds_ratio"] = row_log_odds_ratio
        row_dict["max"] = max_val

        # width of displayed bar
        if isinstance(row_log_odds_ratio, float):
            row_dict["width"] = (
                (abs(row_log_odds_ratio) / max_val) if max_val != 0 else 0
            )
        else:
            row_dict["width"] = 0
        ret.append(row_dict)

    return ret
