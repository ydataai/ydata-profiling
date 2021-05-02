from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.visualisation.plot import scatter_complex


def render_complex(summary):
    varid = summary["varid"]
    template_variables = {}
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Complex number (&Copf;)",
        summary["warnings"],
        summary["description"],
    )
    compute_distinct = config["engine"].get(str) != "spark" or config["spark"][
        "compute_distinct"
    ].get(bool)

    table1 = Table(
        list(
            filter(
                lambda x: x,
                [
                    {
                        "name": "Distinct",
                        "value": summary["n_distinct"],
                        "fmt": "fmt",
                        "alert": "n_distinct" in summary["warn_fields"],
                    }
                    if compute_distinct
                    else None,
                    {
                        "name": "Distinct (%)",
                        "value": summary["p_distinct"],
                        "fmt": "fmt_percent",
                        "alert": "p_distinct" in summary["warn_fields"],
                    }
                    if compute_distinct
                    else None,
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
                        "name": "Memory size",
                        "value": summary["memory_size"],
                        "fmt": "fmt_bytesize",
                        "alert": False,
                    },
                ],
            )
        )
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
        [info, table1, table2, placeholder], sequence_type="grid"
    )

    # Bottom
    items = [
        Image(
            scatter_complex(summary["scatter_data"]),
            image_format=image_format,
            alt="Scatterplot",
            caption="Scatterplot in the complex plane",
            name="Scatter",
            anchor_id=f"{varid}scatter",
        )
    ]

    bottom = Container(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables
