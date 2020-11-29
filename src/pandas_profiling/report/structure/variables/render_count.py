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


def render_count(summary):
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Real number (&Ropf; / &Ropf;<sub>&ge;0</sub>)",
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
                "alert": False,
            },
            {
                "name": "Zeros (%)",
                "value": summary["p_zeros"],
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

    seqs = [
        Image(
            histogram(*summary["histogram"]),
            image_format=image_format,
            alt="Histogram",
            caption=f"<strong>Histogram with fixed size bins</strong> (bins={len(summary['histogram'][1]) - 1})",
            name="Histogram",
            anchor_id="histogram",
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common values",
        anchor_id="common_values",
        redact=False,
    )

    evs = Container(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name="Minimum 5 values",
                anchor_id="firstn",
                redact=False,
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name="Maximum 5 values",
                anchor_id="lastn",
                redact=False,
            ),
        ],
        sequence_type="tabs",
        name="Extreme values",
        anchor_id="extreme_values",
    )

    template_variables["bottom"] = Container(
        [
            Container(
                seqs, sequence_type="tabs", name="Histogram(s)", anchor_id="histograms"
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    return template_variables
