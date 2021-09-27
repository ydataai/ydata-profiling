from typing import List

from pandas_profiling.config import Settings
from pandas_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    FrequencyTableSmall,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import pie_plot


def render_boolean(config: Settings, summary: dict) -> dict:
    varid = summary["varid"]
    n_obs_bool = config.vars.bool.n_obs
    image_format = config.plot.image_format

    # Prepare variables
    template_variables = render_common(config, summary)

    # Element composition
    info = VariableInfo(
        anchor_id=summary["varid"],
        alerts=summary["alerts"],
        var_type="Boolean",
        var_name=summary["varname"],
        description=summary["description"],
    )

    table = Table(
        [
            {
                "name": "Distinct",
                "value": fmt(summary["n_distinct"]),
                "alert": "n_distinct" in summary["alert_fields"],
            },
            {
                "name": "Distinct (%)",
                "value": fmt_percent(summary["p_distinct"]),
                "alert": "p_distinct" in summary["alert_fields"],
            },
            {
                "name": "Missing",
                "value": fmt(summary["n_missing"]),
                "alert": "n_missing" in summary["alert_fields"],
            },
            {
                "name": "Missing (%)",
                "value": fmt_percent(summary["p_missing"]),
                "alert": "p_missing" in summary["alert_fields"],
            },
            {
                "name": "Memory size",
                "value": fmt_bytesize(summary["memory_size"]),
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

    items: List[Renderable] = [
        FrequencyTable(
            template_variables["freq_table_rows"],
            name="Common Values",
            anchor_id=f"{varid}frequency_table",
            redact=False,
        )
    ]

    max_unique = config.plot.pie.max_unique
    if max_unique > 0:
        items.append(
            Image(
                pie_plot(
                    config,
                    summary["value_counts_without_nan"],
                    legend_kws={"loc": "upper right"},
                ),
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
