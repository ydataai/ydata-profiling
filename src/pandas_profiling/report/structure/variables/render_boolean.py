from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    FrequencyTableSmall,
    Table,
    VariableInfo,
)
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_common import render_common


def render_boolean(summary):
    varid = summary["varid"]
    n_obs_bool = config["vars"]["bool"]["n_obs"].get(int)

    # Prepare variables
    template_variables = render_common(summary)
    mini_freq_table_rows = freq_table(
        freqtable=summary["value_counts"],
        n=summary["n"],
        max_number_to_print=n_obs_bool,
    )

    # Element composition
    info = VariableInfo(
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
                "alert": "n_unique" in summary["warn_fields"],
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "alert": "p_unique" in summary["warn_fields"],
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "alert": "n_missing" in summary["warn_fields"],
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "alert": "p_missing" in summary["warn_fields"],
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    fqm = FrequencyTableSmall(mini_freq_table_rows)

    template_variables["top"] = Container([info, table, fqm], sequence_type="grid")

    freqtable = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Frequency Table",
        anchor_id=f"{varid}frequency_table",
    )

    template_variables["bottom"] = Container(
        [freqtable], sequence_type="tabs", anchor_id=f"{varid}bottom"
    )

    return template_variables
