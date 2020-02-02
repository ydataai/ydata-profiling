from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.presentation.core import (
    Preview,
    Sequence,
    Table,
    FrequencyTableSmall,
    FrequencyTable,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common


def render_boolean(summary):
    n_obs_bool = config["vars"]["bool"]["n_obs"].get(int)

    # Prepare variables
    template_variables = render_common(summary)
    mini_freq_table_rows = freq_table(
        freqtable=summary["value_counts"],
        n=summary["n"],
        max_number_to_print=n_obs_bool,
    )

    # Element composition
    info = Overview(
        anchor_id=summary["varid"],
        warnings=summary["warnings"],
        var_type="Boolean",
        var_name=summary["varname"],
    )

    table = Table(
        [
            {
                "name": "Distinct count",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "class": "alert" if "n_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "class": "alert" if "n_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    fqm = FrequencyTableSmall(mini_freq_table_rows)

    template_variables["top"] = Sequence([info, table, fqm], sequence_type="grid")

    freqtable = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Frequency Table",
        anchor_id="{varid}frequency_table".format(varid=summary["varid"]),
    )

    template_variables["bottom"] = Sequence(
        [freqtable],
        sequence_type="tabs",
        anchor_id="{varid}bottom".format(varid=summary["varid"]),
    )

    return template_variables
