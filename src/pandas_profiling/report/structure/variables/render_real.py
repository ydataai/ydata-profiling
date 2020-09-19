from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Table,
    VariableInfo,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import (
    boxplot,
    histogram,
    kde,
    qq_plot,
    render_plot,
)


def render_real(summary):
    varid = summary["varid"]
    template_variables = render_common(summary)

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
        ]
    )

    table2 = Table(
        [
            {
                "name": "Mean",
                "value": summary["mean"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
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
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    plot_obj = histogram(summary["value_counts"])

    mini_histo = render_plot(
        plot_obj,
        name="mini histogram",
        alt="Histogram",
        anchor_id=f"{varid}mini_histo",
    )

    template_variables["top"] = Container(
        [info, table1, table2, mini_histo], sequence_type="top"
    )

    quantile_statistics = Table(
        [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt_numeric"},
            {
                "name": "5-th percentile",
                "value": summary["quantiles"][0.05],
                "fmt": "fmt_numeric",
            },
            {"name": "Q1", "value": summary["quantiles"][0.25], "fmt": "fmt_numeric"},
            {
                "name": "median",
                "value": summary["quantiles"][0.50],
                "fmt": "fmt_numeric",
            },
            {"name": "Q3", "value": summary["quantiles"][0.75], "fmt": "fmt_numeric"},
            {
                "name": "95-th percentile",
                "value": summary["quantiles"][0.95],
                "fmt": "fmt_numeric",
            },
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

    plts = Container(
        [
            render_plot(
                plot_obj,
                alt="Histogram",
                caption=f"<strong>Histogram with fixed size bins</strong>",
                name="Histogram",
                anchor_id=f"{varid}histogram",
            ),
            render_plot(
                boxplot(
                    summary["varname"],
                    summary["min"],
                    summary["quantiles"][0.25],
                    summary["quantiles"][0.50],
                    summary["quantiles"][0.75],
                    summary["max"],
                ),
                alt="Boxplot",
                anchor_id=f"{varid}boxplot",
                name="Boxplot",
            ),
            render_plot(
                kde(summary["data"]),
                alt="Kernel Density Estimation",
                anchor_id=f"{varid}kde",
                name="Kernel Density Estimation",
            ),
        ],
        sequence_type="grid",
        name="Plots",
        anchor_id=f"{varid}plots",
    )

    qqs = Container(
        [
            render_plot(
                qq_plot(summary["quantiles"], "normal"),
                alt="Q-Q Normal",
                anchor_id=f"{varid}qqn",
                name="Q-Q Normal Distribution",
            ),
            render_plot(
                qq_plot(summary["quantiles"], "uniform"),
                alt="Q-Q Uniform",
                anchor_id=f"{varid}qqu",
                name="Q-Q Uniform Distribution",
            ),
        ],
        sequence_type="grid",
        name="Q-Q Plots",
        anchor_id=f"{varid}qqs",
    )

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id=f"{varid}common_values",
        redact=False,
    )
    items = [statistics, plts, qqs]

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

    items += [fq, evs]

    template_variables["bottom"] = Container(
        items,
        sequence_type="tabs",
        anchor_id=f"{varid}bottom",
    )

    return template_variables
