from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import FrequencyTable, Image
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_categorical import (
    render_categorical,
)
from pandas_profiling.visualisation.plot import histogram


def render_path(summary):
    varid = summary["varid"]
    n_freq_table_max = config["n_freq_table_max"].get(int)
    image_format = config["plot"]["image_format"].get(str)

    template_variables = render_categorical(summary)

    keys = ["name", "parent", "suffix", "stem"]
    for path_part in keys:
        template_variables[f"freqtable_{path_part}"] = freq_table(
            freqtable=summary[f"{path_part}_counts"],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        )

    # Top
    template_variables["top"].content["items"][0].content["var_type"] = "Path"
    # TODO: colspan=2
    # template_variables['top'].content['items'][1].content['rows'].append({'name': 'Common prefix', 'value': summary['common_prefix'], 'fmt': 'fmt'})
    # {  # <td>#}
    #     {  # <div style="white-space: nowrap;overflow: hidden;text-overflow: ellipsis;max-width: 600px;">#}
    #         {  # {{ values['common_prefix'] }}#}
    #             {  # </div>#}
    #                 {  # </td>#}
    #
    # Bottom
    full = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Full",
        anchor_id=f"{varid}full_frequency",
    )

    stem = FrequencyTable(
        template_variables["freqtable_stem"],
        name="Stem",
        anchor_id=f"{varid}stem_frequency",
    )

    name = FrequencyTable(
        template_variables["freqtable_name"],
        name="Name",
        anchor_id=f"{varid}name_frequency",
    )

    suffix = FrequencyTable(
        template_variables["freqtable_suffix"],
        name="Suffix",
        anchor_id=f"{varid}suffix_frequency",
    )

    parent = FrequencyTable(
        template_variables["freqtable_parent"],
        name="Parent",
        anchor_id=f"{varid}parent_frequency",
    )

    template_variables["bottom"].content["items"].append(full)
    template_variables["bottom"].content["items"].append(stem)
    template_variables["bottom"].content["items"].append(name)
    template_variables["bottom"].content["items"].append(suffix)
    template_variables["bottom"].content["items"].append(parent)

    if "file_sizes" in summary:
        file_size_histogram = Image(
            histogram(summary["file_sizes"], summary, summary["histogram_bins"]),
            image_format=image_format,
            alt="File size",
            caption=f"<strong>Histogram with fixed size bins of file sizes (in bytes)</strong> (bins={summary['histogram_bins']})",
            name="File size",
            anchor_id=f"{varid}file_size_histogram",
        )

        # TODO: in SequeencyItem
        template_variables["bottom"].content["items"].append(file_size_histogram)

    return template_variables
