import pandas as pd

from ydata_profiling.config import Settings
from ydata_profiling.report.formatters import fmt_numeric
from ydata_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    Table,
)
from ydata_profiling.report.presentation.frequency_table_utils import freq_table
from ydata_profiling.report.structure.variables.render_file import render_file
from ydata_profiling.visualisation.plot import scatter_series
from ydata_profiling.i18n import _


def render_image(config: Settings, summary: dict) -> dict:
    varid = summary["varid"]
    n_freq_table_max = config.n_freq_table_max
    redact = config.vars.cat.redact

    template_variables = render_file(config, summary)

    # Top
    template_variables["top"].content["items"][0].content["var_type"] = "Image"

    # Bottom
    image_items = []

    """
    Min Width           Min Height          Min Area
    Mean Width          Mean Height         Mean Height
    Median Width        Median Height       Median Height
    Max Width           Max Height          Max Height

    All dimension properties are in pixels.
    """

    image_shape_items = [
        Container(
            [
                Table(
                    [
                        {
                            "name": _("core.structure.overview.min_width"),
                            "value": fmt_numeric(
                                summary["min_width"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.median_width"),
                            "value": fmt_numeric(
                                summary["median_width"],
                                precision=config.report.precision,
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.max_width"),
                            "value": fmt_numeric(
                                summary["max_width"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                    ],
                    style=config.html.style,
                ),
                Table(
                    [
                        {
                            "name": _("core.structure.overview.min_height"),
                            "value": fmt_numeric(
                                summary["min_height"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.median_height"),
                            "value": fmt_numeric(
                                summary["median_height"],
                                precision=config.report.precision,
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.max_height"),
                            "value": fmt_numeric(
                                summary["max_height"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                    ],
                    style=config.html.style,
                ),
                Table(
                    [
                        {
                            "name": _("core.structure.overview.min_area"),
                            "value": fmt_numeric(
                                summary["min_area"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.median_area"),
                            "value": fmt_numeric(
                                summary["median_area"],
                                precision=config.report.precision,
                            ),
                            "alert": False,
                        },
                        {
                            "name": _("core.structure.overview.max_area"),
                            "value": fmt_numeric(
                                summary["max_area"], precision=config.report.precision
                            ),
                            "alert": False,
                        },
                    ],
                    style=config.html.style,
                ),
            ],
            anchor_id=f"{varid}tbl",
            name=_("core.structure.overview.overview"),
            sequence_type="grid",
        ),
        Image(
            scatter_series(config, summary["image_dimensions"]),
            image_format=config.plot.image_format,
            alt=_("core.structure.overview.scatter_plot_image_sizes"),
            caption=_("core.structure.overview.scatter_plot_image_sizes"),
            name=_("core.structure.overview.scatter_plot"),
            anchor_id=f"{varid}image_dimensions_scatter",
        ),
        FrequencyTable(
            freq_table(
                freqtable=summary["image_dimensions"].value_counts(),
                n=summary["n"],
                max_number_to_print=n_freq_table_max,
            ),
            name=_("core.structure.overview.common_values"),
            anchor_id=f"{varid}image_dimensions_frequency",
            redact=False,
        ),
    ]

    image_shape = Container(
        image_shape_items,
        sequence_type="named_list",
        name=_("core.structure.overview.dimensions"),
        anchor_id=f"{varid}image_dimensions",
    )

    if "exif_keys_counts" in summary:
        items = [
            FrequencyTable(
                freq_table(
                    freqtable=pd.Series(summary["exif_keys_counts"]),
                    n=summary["n"],
                    max_number_to_print=n_freq_table_max,
                ),
                name=_("core.structure.overview.exif_keys"),
                anchor_id=f"{varid}exif_keys",
                redact=redact,
            )
        ]
        for key, counts in summary["exif_data"].items():
            if key == "exif_keys":
                continue

            items.append(
                FrequencyTable(
                    freq_table(
                        freqtable=counts,
                        n=summary["n"],
                        max_number_to_print=n_freq_table_max,
                    ),
                    name=key,
                    anchor_id=f"{varid}_exif_{key}",
                    redact=redact,
                )
            )

        image_items.append(
            Container(
                items,
                anchor_id=f"{varid}exif_data",
                name=_("core.structure.overview.exif_data"),
                sequence_type="named_list",
            )
        )

    image_items.append(image_shape)

    image_tab = Container(
        image_items,
        name=_("core.structure.overview.image"),
        sequence_type="tabs",
        anchor_id=f"{varid}image",
    )

    template_variables["bottom"].content["items"].append(image_tab)

    return template_variables
