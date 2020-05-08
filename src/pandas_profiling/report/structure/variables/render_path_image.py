import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import Container, FrequencyTable
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_path import render_path


def render_path_image(summary):
    varid = summary["varid"]
    n_freq_table_max = config["n_freq_table_max"].get(int)
    # image_format = config["plot"]["image_format"].get(str)

    template_variables = render_path(summary)

    # Top
    template_variables["top"].content["items"][0].content["var_type"] = "Image Path"

    # Bottom
    keys = {"Image shape": "image_shape", "Exif keys": "exif_keys"}

    for title, key in keys.items():
        template_variables[f"freqtable_{key}"] = freq_table(
            freqtable=pd.Series(summary[f"{key}_counts"]),
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        )

    # TODO: add dropdown to switch to specific values
    exif_keys = FrequencyTable(
        template_variables["freqtable_exif_keys"],
        name="Exif data",
        anchor_id=f"{varid}exif_frequency",
    )

    image_shape_freq = FrequencyTable(
        template_variables["freqtable_image_shape"],
        name="Dimensions",
        anchor_id=f"{varid}image_shape_frequency",
    )

    # TODO: obtain raw image shapes for scatter
    # image_shape_scatter = Image(
    #     scatter_series(summary["scatter_data"]),
    #     image_format=image_format,
    #     alt="Scatterplot of image sizes",
    #     caption="Scatterplot of image sizes",
    #     name="Scatter",
    #     anchor_id=f"{varid}scatter",
    # )

    # image_shape = Container(
    #     [image_shape_freq
    #      , image_shape_scatter
    #     ],
    #     sequence_type="tabs",
    #     name="Dimensions",
    #     anchor_id=f"{varid}image_shape",
    # )

    image_tab = Container(
        [image_shape_freq, exif_keys],
        name="Image",
        sequence_type="tabs",
        anchor_id=f"{varid}image",
    )

    template_variables["bottom"].content["items"].append(image_tab)

    return template_variables
