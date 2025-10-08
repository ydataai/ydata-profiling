from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import (
    fmt,
    fmt_bytesize,
    fmt_numeric,
    fmt_percent,
)
from ydata_profiling.report.presentation.core import (
    HTML,
    Container,
    Image,
    Table,
    VariableInfo,
)
from ydata_profiling.visualisation.plot import scatter_complex
from ydata_profiling.i18n import _


def render_complex(config: Settings, summary: dict) -> dict:
    varid = summary["varid"]
    template_variables = {}
    image_format = config.plot.image_format

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Complex number (&Copf;)",
        summary["alerts"],
        summary["description"],
        style=config.html.style,
    )

    table1 = Table(
        [
            {"name": _("core.structure.overview.distinct"), "value": fmt(summary["n_distinct"])},
            {
                "name": _("core.structure.overview.distinct_percentage"),
                "value": fmt_percent(summary["p_distinct"]),
            },
            {"name": _("core.structure.overview.missing"), "value": fmt(summary["n_missing"])},
            {
                "name": _("core.structure.overview.missing_percentage"),
                "value": fmt_percent(summary["p_missing"]),
            },
            {
                "name": _("core.structure.overview.memory_size"),
                "value": fmt_bytesize(summary["memory_size"]),
            },
        ],
        style=config.html.style,
    )

    table2 = Table(
        [
            {
                "name": _("core.structure.overview.mean"),
                "value": fmt_numeric(
                    summary["mean"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.min"),
                "value": fmt_numeric(summary["min"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.max"),
                "value": fmt_numeric(summary["max"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.zeros"),
                "value": fmt_numeric(
                    summary["n_zeros"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.zeros_percentage"),
                "value": fmt_percent(summary["p_zeros"])
            },
        ],
        style=config.html.style,
    )

    placeholder = HTML("")

    template_variables["top"] = Container(
        [info, table1, table2, placeholder], sequence_type="grid"
    )

    # Bottom
    items = [
        Image(
            scatter_complex(config, summary["scatter_data"]),
            image_format=image_format,
            alt= _("core.structure.overview.scatterplot"),
            caption=_("core.structure.overview.scatterplot_caption"),
            name=_("core.structure.overview.scatter"),
            anchor_id=f"{varid}scatter",
        )
    ]

    bottom = Container(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables
