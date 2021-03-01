from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import histogram, mini_histogram


def render_real(summary):
    varid = summary["varid"]
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    if summary["min"] >= 0:
        name = "Real number (&Ropf;<sub>&ge;0</sub>)"
    else:
        name = "Real number (&Ropf;)"

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        name,
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
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
                "name": "Infinite",
                "value": summary["n_infinite"],
                "fmt": "fmt",
                "alert": "n_infinite" in summary["warn_fields"],
            },
            {
                "name": "Infinite (%)",
                "value": summary["p_infinite"],
                "fmt": "fmt_percent",
                "alert": "p_infinite" in summary["warn_fields"],
            },
            {
                "name": "Mean",
                "value": summary["mean"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
        ]
    )

    table2 = Table(
        [
            {
                "name": "Minimum",
                "value": summary["min"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Maximum",
                "value": summary["max"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Zeros",
                "value": summary["n_zeros"],
                "fmt": "fmt",
                "alert": "n_zeros" in summary["warn_fields"],
            },
            {
                "name": "Zeros (%)",
                "value": summary["p_zeros"],
                "fmt": "fmt_percent",
                "alert": "p_zeros" in summary["warn_fields"],
            },
            {
                "name": "Negative",
                "value": summary["n_negative"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "Negative (%)",
                "value": summary["p_negative"],
                "fmt": "fmt_percent",
                "alert": False,
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    mini_histo = Image(
        mini_histogram(*summary["histogram"]),
        image_format=image_format,
        alt="Mini histogram",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": "5-th percentile", "value": summary["5%"], "fmt": "fmt_numeric"},
            {"name": "Q1", "value": summary["25%"], "fmt": "fmt_numeric"},
            {"name": "median", "value": summary["50%"], "fmt": "fmt_numeric"},
            {"name": "Q3", "value": summary["75%"], "fmt": "fmt_numeric"},
            {"name": "95-th percentile", "value": summary["95%"], "fmt": "fmt_numeric"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "Range", "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": "Interquartile range (IQR)",
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
        name="Quantile statistics",
    )

    if summary["monotonic_increase_strict"]:
        monotocity = "Strictly increasing"
    elif summary["monotonic_decrease_strict"]:
        monotocity = "Strictly decreasing"
    elif summary["monotonic_increase"]:
        monotocity = "Increasing"
    elif summary["monotonic_decrease"]:
        monotocity = "Decreasing"
    else:
        monotocity = "Not monotonic"

    descriptive_statistics = Table(
        [
            {
                "name": "Standard deviation",
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Coefficient of variation (CV)",
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": "Kurtosis", "value": summary["kurtosis"], "fmt": "fmt_numeric"},
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt_numeric"},
            {
                "name": "Median Absolute Deviation (MAD)",
                "value": summary["mad"],
                "fmt": "fmt_numeric",
            },
            {
                "name": "Skewness",
                "value": summary["skewness"],
                "fmt": "fmt_numeric",
                "class": "alert" if "skewness" in summary["warn_fields"] else "",
            },
            {"name": "Sum", "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": "Variance", "value": summary["variance"], "fmt": "fmt_numeric"},
            {"name": "Monotocity", "value": monotocity, "fmt": "fmt"},
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
        histogram(*summary["histogram"]),
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
                name="Minimum 5 values",
                anchor_id=f"{varid}firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="Maximum 5 values",
                anchor_id=f"{varid}lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name="Extreme values",
        anchor_id=f"{varid}extreme_values",
    )

    template_variables["bottom"] = Container(
        [statistics, hist, fq, evs],
        sequence_type="tabs",
        anchor_id=f"{varid}bottom",
    )

    return template_variables
