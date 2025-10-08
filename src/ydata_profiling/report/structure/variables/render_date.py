from typing import Any, Dict

from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from ydata_profiling.report.presentation.core import (
    Container,
    Image,
    Table,
    VariableInfo,
)
from ydata_profiling.visualisation.plot import histogram, mini_histogram
from ydata_profiling.i18n import _


def render_date(config: Settings, summary: Dict[str, Any]) -> Dict[str, Any]:
    varid = summary["varid"]
    template_variables = {}

    image_format = config.plot.image_format

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Date",
        summary["alerts"],
        summary["description"],
        style=config.html.style,
    )

    table1 = Table(
        [
            {
                "name": _("core.structure.overview.distinct"),
                "value": fmt(summary["n_distinct"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.distinct_percentage"),
                "value": fmt_percent(summary["p_distinct"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.missing"),
                "value": fmt(summary["n_missing"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.missing_percentage"),
                "value": fmt_percent(summary["p_missing"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.memory_size"),
                "value": fmt_bytesize(summary["memory_size"]),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    table2 = Table(
        [
            {"name": _("core.structure.overview.min"), "value": fmt(summary["min"]), "alert": False},
            {"name": _("core.structure.overview.max"), "value": fmt(summary["max"]), "alert": False},
            {
                "name": _("core.structure.overview.invalid_dates"),
                "value": fmt(summary["n_invalid_dates"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.invalid_dates_percentage"),
                "value": fmt_percent(summary["p_invalid_dates"]),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    if isinstance(summary["histogram"], list):
        mini_histo = Image(
            mini_histogram(
                config,
                [x[0] for x in summary["histogram"]],
                [x[1] for x in summary["histogram"]],
                date=True,
            ),
            image_format=image_format,
            alt=_("core.structure.overview.mini_histogram"),
        )
    else:
        mini_histo = Image(
            mini_histogram(
                config, summary["histogram"][0], summary["histogram"][1], date=True
            ),
            image_format=image_format,
            alt=_("core.structure.overview.mini_histogram"),
        )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    if isinstance(summary["histogram"], list):
        hist_data = histogram(
            config,
            [x[0] for x in summary["histogram"]],
            [x[1] for x in summary["histogram"]],
            date=True,
        )
    else:
        hist_data = histogram(
            config, summary["histogram"][0], summary["histogram"][1], date=True
        )

    # Bottom
    n_bins = len(summary["histogram"][1]) - 1 if summary["histogram"] else 0
    bottom = Container(
        [
            Image(
                hist_data,
                image_format=image_format,
                alt=_("core.structure.overview.histogram"),
                caption=f"<strong>{_("core.structure.overview.histogram_caption")}</strong> (bins={n_bins})",
                name=_("core.structure.overview.histogram"),
                anchor_id=f"{varid}histogram",
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
