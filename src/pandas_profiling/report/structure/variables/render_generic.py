from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Table,
    VariableInfo,
)


def render_generic(summary):
    info = VariableInfo(
        anchor_id=summary["varid"],
        warnings=summary["warnings"],
        var_type="Unsupported",
        var_name=summary["varname"],
        description=summary["description"],
    )

    table = Table(
        [
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
        ]
    )

    return {
        "top": Container([info, table, HTML("")], sequence_type="grid"),
        "bottom": None,
    }
