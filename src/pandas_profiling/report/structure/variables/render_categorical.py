import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.visualisation.plot import histogram
from pandas_profiling.report.presentation.core import (
    Image,
    FrequencyTable,
    FrequencyTableSmall,
    Preview,
    Sequence,
    Table,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common


def render_categorical(summary):
    n_obs_cat = config["vars"]["cat"]["n_obs"].get(int)

    template_variables = render_common(summary)

    # TODO: merge with boolean
    mini_freq_table_rows = freq_table(
        freqtable=summary["value_counts"],
        n=summary["count"],
        max_number_to_print=n_obs_cat,
    )

    # Top
    # Element composition
    info = Overview(
        summary["varid"], summary["varname"], "Categorical", summary["warnings"]
    )

    table = Table(
        [
            {
                "name": "Distinct count",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "class": "alert" if "n_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_unique" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing",
                "value": summary["n_missing"],
                "fmt": "fmt",
                "class": "alert" if "n_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Missing (%)",
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_missing" in summary["warn_fields"] else "",
            },
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    fqm = FrequencyTableSmall(mini_freq_table_rows)

    # TODO: settings 3,3,6
    template_variables["top"] = Sequence([info, table, fqm], sequence_type="grid")

    # Bottom
    items = []
    frequency_table = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common Values",
        anchor_id="{varid}common_values".format(varid=summary["varid"]),
    )

    items.append(frequency_table)

    check_compositions = config["vars"]["cat"]["check_composition"].get(bool)
    if check_compositions:
        length_table = Table(
            [
                {
                    "name": "Max length",
                    "value": summary["max_length"],
                    "fmt": "fmt_numeric",
                },
                {
                    "name": "Mean length",
                    "value": summary["mean_length"],
                    "fmt": "fmt_numeric",
                },
                {
                    "name": "Min length",
                    "value": summary["min_length"],
                    "fmt": "fmt_numeric",
                },
            ],
            name="Length",
            anchor_id="{varid}lengthstats".format(varid=summary["varid"]),
        )

        histogram_bins = 10

        length = Image(
            histogram(summary["length"], summary, histogram_bins),
            alt="Scatter",
            name="Length",
            anchor_id="{varid}length".format(varid=summary["varid"]),
        )

        tbl = Sequence(
            [length, length_table],
            anchor_id="{varid}tbl".format(varid=summary["varid"]),
            name="Length",
            sequence_type="grid",
        )

        items.append(tbl)

        n_freq_table_max = config["n_freq_table_max"].get(int)

        citems = []
        vc = pd.Series(summary["category_alias_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Categories",
                anchor_id="{varid}category_long_values".format(varid=summary["varid"]),
            )
        )

        vc = pd.Series(summary["script_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Scripts",
                anchor_id="{varid}script_values".format(varid=summary["varid"]),
            )
        )

        vc = pd.Series(summary["block_alias_values"]).value_counts()
        citems.append(
            FrequencyTable(
                freq_table(
                    freqtable=vc, n=vc.sum(), max_number_to_print=n_freq_table_max
                ),
                name="Blocks",
                anchor_id="{varid}block_alias_values".format(varid=summary["varid"]),
            )
        )

        characters = Sequence(
            citems,
            name="Characters",
            sequence_type="tabs",
            anchor_id="{varid}characters".format(varid=summary["varid"]),
        )

        items.append(characters)

    template_variables["bottom"] = Sequence(
        items,
        sequence_type="tabs",
        anchor_id="{varid}bottom".format(varid=summary["varid"]),
    )

    return template_variables
