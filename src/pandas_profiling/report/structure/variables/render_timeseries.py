from pandas_profiling.config import Settings
from pandas_profiling.report.formatters import (
    fmt,
    fmt_bytesize,
    fmt_monotonic,
    fmt_numeric,
    fmt_percent,
)
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import histogram, mini_ts_plot, plot_acf_pacf


def render_timeseries(config: Settings, summary: dict) -> dict:
    varid = summary["varid"]
    template_variables = render_common(config, summary)
    image_format = config.plot.image_format

    if summary["min"] >= 0:
        name = "Numeric time series"
    else:
        name = "Numeric time series"

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        name,
        summary["alerts"],
        summary["description"],
    )

    table1 = Table(
        [
            {
                "name": "Distinct",
                "value": summary["n_distinct"],
                "fmt": fmt,
                "alert": "n_distinct" in summary["alert_fields"],
            },
            {
                "name": "Distinct (%)",
                "value": summary["p_distinct"],
                "fmt": fmt_percent,
                "alert": "p_distinct" in summary["alert_fields"],
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": fmt,
                "alert": "n_missing" in summary["alert_fields"],
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": fmt_percent,
                "alert": "p_missing" in summary["alert_fields"],
            },
            {
                "name": "Infinite",
                "value": summary["n_infinite"],
                "fmt": fmt,
                "alert": "n_infinite" in summary["alert_fields"],
            },
            {
                "name": "Infinite (%)",
                "value": summary["p_infinite"],
                "fmt": fmt_percent,
                "alert": "p_infinite" in summary["alert_fields"],
            },
        ]
    )

    table2 = Table(
        [
            {
                "name": "Mean",
                "value": summary["mean"],
                "fmt": fmt_numeric,
                "alert": False,
            },
            {
                "name": "Minimum",
                "value": summary["min"],
                "fmt": fmt_numeric,
                "alert": False,
            },
            {
                "name": "Maximum",
                "value": summary["max"],
                "fmt": fmt_numeric,
                "alert": False,
            },
            {
                "name": "Zeros",
                "value": summary["n_zeros"],
                "fmt": fmt,
                "alert": "n_zeros" in summary["alert_fields"],
            },
            {
                "name": "Zeros (%)",
                "value": summary["p_zeros"],
                "fmt": fmt_percent,
                "alert": "p_zeros" in summary["alert_fields"],
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": fmt_bytesize,
                "alert": False,
            },
        ]
    )

    mini_plot = Image(
        mini_ts_plot(config, summary["series"]),
        image_format=image_format,
        alt="Mini TS plot",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_plot], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {
                "name": "Minimum",
                "value": fmt_numeric(summary["min"], precision=config.report.precision),
            },
            {
                "name": "5-th percentile",
                "value": fmt_numeric(summary["5%"], precision=config.report.precision),
            },
            {
                "name": "Q1",
                "value": fmt_numeric(summary["25%"], precision=config.report.precision),
            },
            {
                "name": "median",
                "value": fmt_numeric(summary["50%"], precision=config.report.precision),
            },
            {
                "name": "Q3",
                "value": fmt_numeric(summary["75%"], precision=config.report.precision),
            },
            {
                "name": "95-th percentile",
                "value": fmt_numeric(summary["95%"], precision=config.report.precision),
            },
            {
                "name": "Maximum",
                "value": fmt_numeric(summary["max"], precision=config.report.precision),
            },
            {
                "name": "Range",
                "value": fmt_numeric(
                    summary["range"], precision=config.report.precision
                ),
            },
            {
                "name": "Interquartile range (IQR)",
                "value": fmt_numeric(summary["iqr"], precision=config.report.precision),
            },
        ],
        name="Quantile statistics",
    )

    descriptive_statistics = Table(
        [
            {
                "name": "Standard deviation",
                "value": fmt_numeric(summary["std"], precision=config.report.precision),
            },
            {
                "name": "Coefficient of variation (CV)",
                "value": fmt_numeric(summary["cv"], precision=config.report.precision),
            },
            {
                "name": "Kurtosis",
                "value": fmt_numeric(
                    summary["kurtosis"], precision=config.report.precision
                ),
            },
            {
                "name": "Mean",
                "value": fmt_numeric(
                    summary["mean"], precision=config.report.precision
                ),
            },
            {
                "name": "Median Absolute Deviation (MAD)",
                "value": fmt_numeric(summary["mad"], precision=config.report.precision),
            },
            {
                "name": "Skewness",
                "value": fmt_numeric(
                    summary["skewness"], precision=config.report.precision
                ),
                "class": "alert" if "skewness" in summary["alert_fields"] else "",
            },
            {
                "name": "Sum",
                "value": fmt_numeric(summary["sum"], precision=config.report.precision),
            },
            {
                "name": "Variance",
                "value": fmt_numeric(
                    summary["variance"], precision=config.report.precision
                ),
            },
            {
                "name": "Monotonicity",
                "value": fmt_monotonic(summary["monotonic"]),
            },
            {
                "name": "Augmented Dickey-Fuller test p-value",
                "value": fmt_numeric(summary["addfuller"]),
            },
        ],
        name="Descriptive statistics",
    )

    statistics = Container(
        [quantile_statistics, descriptive_statistics],
        anchor_id=f"{varid}statistics",
        name="Statistics",
        sequence_type="grid",
    )

    hist = Image(
        histogram(config, *summary["histogram"]),
        image_format=image_format,
        alt="Histogram",
        caption=f"<strong>Histogram with fixed size bins</strong> (bins={len(summary['histogram'][1]) - 1})",
        name="Histogram",
        anchor_id=f"{varid}histogram",
    )

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id=f"{varid}common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name=f"Minimum {config.n_extreme_obs} values",
                anchor_id=f"{varid}firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name=f"Maximum {config.n_extreme_obs} values",
                anchor_id=f"{varid}lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name="Extreme values",
        anchor_id=f"{varid}extreme_values",
    )

    acf_pacf = Image(
        plot_acf_pacf(config, summary["series"]),
        image_format=image_format,
        alt="Autocorrelation",
        caption="<strong>ACF and PACF</strong>",
        name="Autocorrelation",
        anchor_id=f"{varid}acf_pacf",
    )

    template_variables["bottom"] = Container(
        [statistics, hist, fq, evs, acf_pacf],
        sequence_type="tabs",
        anchor_id=f"{varid}bottom",
    )

    return template_variables
