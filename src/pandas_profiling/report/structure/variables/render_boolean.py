from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    FrequencyTableSmall,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import pie_plot


def render_boolean(summary):
    varid = summary["varid"]
    n_obs_bool = config["vars"]["bool"]["n_obs"].get(int)
    image_format = config["plot"]["image_format"].get(str)

    # Prepare variables
    template_variables = render_common(summary)

    # Element composition
    info = VariableInfo(
        anchor_id=summary["varid"],
        warnings=summary["warnings"],
        var_type="Boolean",
        var_name=summary["varname"],
        description=summary["description"],
    )

    table = Table(
        [
            {
                "name": "Distinct",
                "value": summary["n_distinct"],
                "fmt": "fmt",
                "alert": "n_distinct" in summary["warn_fields"],
            },
            {
                "name": "Distinct (%)",
                "value": summary["p_distinct"],
                "fmt": "fmt_percent",
                "alert": "p_distinct" in summary["warn_fields"],
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

    fqm = FrequencyTableSmall(
        freq_table(
            freqtable=summary["value_counts_without_nan"],
            n=summary["n"],
            max_number_to_print=n_obs_bool,
        ),
        redact=False,
    )

    template_variables["top"] = Container([info, table, fqm], sequence_type="grid")

    items = [
        FrequencyTable(
            template_variables["freq_table_rows"],
            name="Common Values",
            anchor_id=f"{varid}frequency_table",
            redact=False,
        )
    ]

    max_unique = config["plot"]["pie"]["max_unique"].get(int)
    if max_unique > 0:
        items.append(
            Image(
                pie_plot(summary["value_counts_without_nan"], legend_kws={"loc": "upper right"}),
                image_format=image_format,
                alt="Chart",
                name="Chart",
                anchor_id=f"{varid}pie_chart",
            )
        )

    template_variables["bottom"] = Container(
        items, sequence_type="tabs", anchor_id=f"{varid}bottom"
    )

    return template_variables
