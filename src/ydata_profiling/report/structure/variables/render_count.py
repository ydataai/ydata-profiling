from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import (
    fmt,
    fmt_bytesize,
    fmt_numeric,
    fmt_percent,
)
from ydata_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
    VariableInfo,
)
from ydata_profiling.report.structure.variables.render_common import render_common
from ydata_profiling.visualisation.plot import histogram, mini_histogram
from ydata_profiling.i18n import _


def render_count(config: Settings, summary: dict) -> dict:
    template_variables = render_common(config, summary)
    image_format = config.plot.image_format

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Real number (&Ropf; / &Ropf;<sub>&ge;0</sub>)",
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
                "alert": False,
            },
            {
                "name": _("core.structure.overview.min"),
                "value": fmt_numeric(summary["min"], precision=config.report.precision),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.max"),
                "value": fmt_numeric(summary["max"], precision=config.report.precision),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.zeros"),
                "value": fmt(summary["n_zeros"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.zeros_percentage"),
                "value": fmt_percent(summary["p_zeros"]),
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

    mini_histo = Image(
        mini_histogram(config, *summary["histogram"]),
        image_format=image_format,
        alt=_("core.structure.overview.mini_histogram"),
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    seqs = [
        Image(
            histogram(config, *summary["histogram"]),
            image_format=image_format,
            alt=_("core.structure.overview.histogram"),
            caption=f"<strong>{_("core.structure.overview.histogram_caption")}</strong> (bins={len(summary['histogram'][1]) - 1})",
            name=_("core.structure.overview.histogram"),
            anchor_id="histogram",
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name=_("core.structure.overview.common_values"),
        anchor_id="common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name=f"{_("core.structure.overview.min")} {config.n_extreme_obs} {_("core.structure.overview.values")}",
                anchor_id="firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name=f"{_("core.structure.overview.max")} {config.n_extreme_obs} {_("core.structure.overview.values")}",
                anchor_id="lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name=_("core.structure.overview.extreme_values"),
        anchor_id="extreme_values",
    )

    template_variables["bottom"] = Container(
        [
            Container(
                seqs, sequence_type="tabs", name=_("core.structure.overview.histogram_s"), anchor_id="histograms"
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    return template_variables
