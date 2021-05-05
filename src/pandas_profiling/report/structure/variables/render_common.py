from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import (
    extreme_obs_table,
    freq_table,
)


def render_common(summary):
    n_extreme_obs = config["n_extreme_obs"].get(int)
    n_freq_table_max = config["n_freq_table_max"].get(int)

    sorted_freqtable = summary["value_counts_without_nan"].sort_index(ascending=True)

    template_variables = {
        # TODO: with nan
        "freq_table_rows": freq_table(
            freqtable=summary["value_counts_without_nan"],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        ),
        "firstn_expanded": extreme_obs_table(
            freqtable=sorted_freqtable,
            number_to_print=n_extreme_obs,
            n=summary["n"],
        ),
        "lastn_expanded": extreme_obs_table(
            freqtable=sorted_freqtable[::-1],
            number_to_print=n_extreme_obs,
            n=summary["n"],
        ),
    }

    return template_variables
