from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Table,
    VariableInfo,
)
from pandas_profiling.visualisation.plot import render_plot  # , scatter_complex


def render_complex(summary):
    varid = summary["varid"]
    template_variables = {}

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Complex number (&Copf;)",
        summary["warnings"],
        summary["description"],
    )

    table1 = Table(
        [
            {"name": "Distinct", "value": summary["n_distinct"], "fmt": "fmt"},
            {
                "name": "Distinct (%)",
                "value": summary["p_distinct"],
                "fmt": "fmt_percent",
            },
            {"name": "Missing", "value": summary["n_missing"], "fmt": "fmt"},
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    table2 = Table(
        [
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt_numeric"},
            {"name": "Minimum", "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": "Maximum", "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": "Zeros", "value": summary["n_zeros"], "fmt": "fmt_numeric"},
            {"name": "Zeros (%)", "value": summary["p_zeros"], "fmt": "fmt_percent"},
        ]
    )

    placeholder = HTML("")

    template_variables["top"] = Container(
        [info, table1, table2, placeholder], sequence_type="top"
    )

    # Bottom
    items = [
        render_plot(
            scatter_complex(summary["scatter_data"]),
            alt="Scatterplot",
            caption="Scatterplot in the complex plane",
            name="Scatter",
            anchor_id=f"{varid}scatter",
        )
    ]

    bottom = Container(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables
