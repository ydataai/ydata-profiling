from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import Container, Table, VariableInfo
from pandas_profiling.visualisation.plot import histogram, render_plot


def render_date(summary):
    varid = summary["varid"]
    template_variables = {}

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Date",
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
        [
            {
                "name": "Distinct",
                "value": summary["n_distinct"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "Distinct (%)",
                "value": summary["p_distinct"],
                "fmt": "fmt_percent",
                "alert": False,
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
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

    table2 = Table(
        [
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt", "alert": False},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt", "alert": False},
        ]
    )

    histo = render_plot(
        histogram(summary["value_counts_without_nan"], date=True),
        alt="Histogram",
        caption=f"<strong>Histogram with fixed size bins</strong>",
        name="Histogram",
        anchor_id=f"{varid}histogram",
    )

    template_variables["top"] = Container(
        [info, table1, table2, histo], sequence_type="top"
    )

    # Bottom
    bottom = Container(
        [histo],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
