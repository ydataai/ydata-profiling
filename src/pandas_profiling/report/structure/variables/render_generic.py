from pandas_profiling.config import Settings
from pandas_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from pandas_profiling.report.presentation.core import (
    HTML,
    Container,
    Table,
    VariableInfo,
)


def render_generic(config: Settings, summary: dict) -> dict:
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
                "value": fmt(summary["n_missing"]),
                "alert": "n_missing" in summary["warn_fields"],
            },
            {
                "name": "Missing (%)",
                "value": fmt_percent(summary["p_missing"]),
                "alert": "p_missing" in summary["warn_fields"],
            },
            {
                "name": "Memory size",
                "value": fmt_bytesize(summary["memory_size"]),
                "alert": False,
            },
        ]
    )

    return {
        "top": Container([info, table, HTML("")], sequence_type="grid"),
        "bottom": None,
    }
