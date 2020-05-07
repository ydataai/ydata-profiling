from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import Container, FrequencyTable, Image
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_path import render_path
from pandas_profiling.visualisation.plot import scatter_series


def render_path_image(summary):
    varid = summary["varid"]
    n_freq_table_max = config["n_freq_table_max"].get(int)
    image_format = config["plot"]["image_format"].get(str)

    template_variables = render_path(summary)

    # Top
    template_variables["top"].content["items"][0].content["var_type"] = "Image Path"

    # Bottom
    keys = {"Image shape": "image_shape", "Exif keys": "exif_keys"}

    for title, key in keys.items():
        template_variables[f"freqtable_{key}"] = freq_table(
            freqtable=summary[f"{key}_counts"],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        )

    # TODO: add dropdown to switch to specific values
    exif_keys = FrequencyTable(
        template_variables["freqtable_exif_keys"],
        name="Exif keys",
        anchor_id=f"{varid}exif_frequency",
    )

    template_variables["bottom"].content["items"].append(exif_keys)

    image_shape_freq = FrequencyTable(
        template_variables["freqtable_image_shape"],
        name="Frequency",
        anchor_id=f"{varid}image_shape_frequency",
    )

    image_shape_scatter = Image(
        scatter_series(summary["scatter_data"]),
        image_format=image_format,
        alt="Scatterplot of image sizes",
        caption="Scatterplot of image sizes",
        name="Scatter",
        anchor_id=f"{varid}scatter",
    )

    image_shape = Container(
        [image_shape_freq, image_shape_scatter],
        sequence_type="tabs",
        name="Image shape",
        anchor_id=f"{varid}image_shape",
    )

    template_variables["bottom"].content["items"].append(image_shape)

    return template_variables
