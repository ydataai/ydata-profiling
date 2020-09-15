from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import (
    extreme_obs_table,
    freq_table,
)


def render_common(summary):
    n_extreme_obs = config["n_extreme_obs"].get(int)
    n_freq_table_max = config["n_freq_table_max"].get(int)

    template_variables = {
        # TODO: with nan
        "freq_table_rows": freq_table(
            freqtable=summary["value_counts_without_nan"],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        ),
        "firstn_expanded": extreme_obs_table(
            freqtable=summary["value_counts_without_nan"],
            number_to_print=n_extreme_obs,
            n=summary["n"],
            ascending=True,
        ),
        "lastn_expanded": extreme_obs_table(
            freqtable=summary["value_counts_without_nan"],
            number_to_print=n_extreme_obs,
            n=summary["n"],
            ascending=False,
        ),
    }

    return template_variables
