from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import (
    fmt,
    fmt_bytesize,
    fmt_monotonic,
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


def render_real(config: Settings, summary: dict) -> dict:
    varid = summary["varid"]
    template_variables = render_common(config, summary)
    image_format = config.plot.image_format

    name = "Real number (&Ropf;)"

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        name,
        summary["alerts"],
        summary["description"],
        style=config.html.style,
    )

    table1 = Table(
        [
            {
                "name": _("core.structure.overview.distinct"),
                "value": fmt(summary["n_distinct"]),
                "alert": "n_distinct" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.distinct_percentage"),
                "value": fmt_percent(summary["p_distinct"]),
                "alert": "p_distinct" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.missing"),
                "value": fmt(summary["n_missing"]),
                "alert": "n_missing" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.missing_percentage"),
                "value": fmt_percent(summary["p_missing"]),
                "alert": "p_missing" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.infinite"),
                "value": fmt(summary["n_infinite"]),
                "alert": "n_infinite" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.infinite_percentage"),
                "value": fmt_percent(summary["p_infinite"]),
                "alert": "p_infinite" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.mean"),
                "value": fmt_numeric(
                    summary["mean"], precision=config.report.precision
                ),
                "alert": False,
            },
        ],
        style=config.html.style,
    )

    table2 = Table(
        [
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
                "alert": "n_zeros" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.zeros_percentage"),
                "value": fmt_percent(summary["p_zeros"]),
                "alert": "p_zeros" in summary["alert_fields"],
            },
            {
                "name": _("core.structure.overview.Negative"),
                "value": fmt(summary["n_negative"]),
                "alert": False,
            },
            {
                "name": _("core.structure.overview.Negative_percentage"),
                "value": fmt_percent(summary["p_negative"]),
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

    if isinstance(summary.get("histogram", []), list):
        mini_histo = Image(
            mini_histogram(
                config,
                [x[0] for x in summary.get("histogram", [])],
                [x[1] for x in summary.get("histogram", [])],
            ),
            image_format=image_format,
            alt=_("core.structure.overview.mini_histogram"),
        )
    else:
        mini_histo = Image(
            mini_histogram(config, *summary["histogram"]),
            image_format=image_format,
            alt=_("core.structure.overview.mini_histogram"),
        )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {
                "name": _("core.structure.overview.min"),
                "value": fmt_numeric(summary["min"], precision=config.report.precision),
            },
            {
                "name":  _("core.structure.overview.5_th_percentile"),#"5-th percentile",
                "value": fmt_numeric(summary["5%"], precision=config.report.precision),
            },
            {
                "name":  _("core.structure.overview.q1"),
                "value": fmt_numeric(summary["25%"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.median"),
                "value": fmt_numeric(summary["50%"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.q3"),
                "value": fmt_numeric(summary["75%"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.95_th_percentile"),
                "value": fmt_numeric(summary["95%"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.max"),
                "value": fmt_numeric(summary["max"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.range"),
                "value": fmt_numeric(
                    summary["range"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.iqr"),
                "value": fmt_numeric(summary["iqr"], precision=config.report.precision),
            },
        ],
        name=_("core.structure.overview.quantile_statistics"),
        style=config.html.style,
    )

    descriptive_statistics = Table(
        [
            {
                "name": _("core.structure.overview.standard_deviation"),
                "value": fmt_numeric(summary["std"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.cv"),
                "value": fmt_numeric(summary["cv"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.kurtosis"),
                "value": fmt_numeric(
                    summary["kurtosis"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.mean"),
                "value": fmt_numeric(
                    summary["mean"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.mad"),
                "value": fmt_numeric(summary["mad"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.skewness"),
                "value": fmt_numeric(
                    summary["skewness"], precision=config.report.precision
                ),
                "class": "alert" if "skewness" in summary["alert_fields"] else "",
            },
            {
                "name": _("core.structure.overview.sum"),
                "value": fmt_numeric(summary["sum"], precision=config.report.precision),
            },
            {
                "name": _("core.structure.overview.variance"),
                "value": fmt_numeric(
                    summary["variance"], precision=config.report.precision
                ),
            },
            {
                "name": _("core.structure.overview.monotonicity"),
                "value": fmt_monotonic(summary["monotonic"]),
            },
        ],
        name=_("core.structure.overview.descriptive_statistics"),
        style=config.html.style,
    )

    statistics = Container(
        [quantile_statistics, descriptive_statistics],
        anchor_id=f"{varid}statistics",
        name=_("core.structure.overview.statistics"),
        sequence_type="grid",
    )

    if isinstance(summary.get("histogram", []), list):
        hist_data = histogram(
            config,
            [x[0] for x in summary.get("histogram", [])],
            [x[1] for x in summary.get("histogram", [])],
        )
        bins = len(summary["histogram"][0][1]) - 1 if "histogram" in summary else 0
        hist_caption = f"<strong>{_("core.structure.overview.histogram_caption")}</strong> (bins={bins})"
    else:
        hist_data = histogram(config, *summary["histogram"])
        hist_caption = f"<strong>{_("core.structure.overview.histogram_caption")}</strong> (bins={len(summary['histogram'][1]) - 1})"

    hist = Image(
        hist_data,
        image_format=image_format,
        alt=_("core.structure.overview.histogram"),
        caption=hist_caption,
        name=_("core.structure.overview.histogram"),
        anchor_id=f"{varid}histogram",
    )

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name=_("core.structure.overview.common_values"),
        anchor_id=f"{varid}common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name=f"{_("core.structure.overview.min")} {config.n_extreme_obs} {_("core.structure.overview.values")}",
                anchor_id=f"{varid}firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name=f"{_("core.structure.overview.max")} {config.n_extreme_obs} {_("core.structure.overview.values")}",
                anchor_id=f"{varid}lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name=_("core.structure.overview.extreme_values"),
        anchor_id=f"{varid}extreme_values",
    )

    template_variables["bottom"] = Container(
        [statistics, hist, fq, evs],
        sequence_type="tabs",
        anchor_id=f"{varid}bottom",
    )

    return template_variables
