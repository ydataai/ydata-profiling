from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.visualisation.plot import histogram
from pandas_profiling.report.presentation.core import Image, FrequencyTable, Overview
from pandas_profiling.report.structure.variables.render_categorical import (
    render_categorical,
)


def render_path(summary):
    n_freq_table_max = config["n_freq_table_max"].get(int)

    template_variables = render_categorical(summary)

    keys = ["name", "parent", "suffix", "stem"]
    for path_part in keys:
        template_variables["freqtable_{}".format(path_part)] = freq_table(
            freqtable=summary["{}_counts".format(path_part)],
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
        template_variables["freq_table_rows"], name="Full", anchor_id="{varid}full_frequency".format(varid=summary['varid'])
    )

    stem = FrequencyTable(
        template_variables["freqtable_stem"], name="Stem", anchor_id="{varid}stem_frequency".format(varid=summary['varid'])
    )

    name = FrequencyTable(
        template_variables["freqtable_name"], name="Name", anchor_id="{varid}name_frequency".format(varid=summary['varid'])
    )

    suffix = FrequencyTable(
        template_variables["freqtable_suffix"],
        name="Suffix",
        anchor_id="{varid}suffix_frequency".format(varid=summary['varid']),
    )

    parent = FrequencyTable(
        template_variables["freqtable_parent"],
        name="Parent",
        anchor_id="{varid}parent_frequency".format(varid=summary['varid']),
    )

    template_variables["bottom"].content["items"].append(full)
    template_variables["bottom"].content["items"].append(stem)
    template_variables["bottom"].content["items"].append(name)
    template_variables["bottom"].content["items"].append(suffix)
    template_variables["bottom"].content["items"].append(parent)

    if "file_sizes" in summary:
        file_size_histogram = Image(
            histogram(summary["file_sizes"], summary, summary["histogram_bins"]),
            alt="File size",
            caption="<strong>Histogram with fixed size bins of file sizes (in bytes)</strong> (bins={})".format(
                summary["histogram_bins"]
            ),
            name="File size",
            anchor_id="{varid}file_size_histogram".format(varid=summary['varid']),
        )

        # TODO: in SequeencyItem
        template_variables["bottom"].content["items"].append(file_size_histogram)

    return template_variables
