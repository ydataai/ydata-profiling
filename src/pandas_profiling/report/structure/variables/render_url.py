from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    FrequencyTableSmall,
    Table,
    Variable,
    VariableInfo,
)
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables import render_common


def render_url(summary):
    varid = summary["varid"]
    n_freq_table_max = config["n_freq_table_max"].get(int)

    n_obs_cat = config["vars"]["cat"]["n_obs"].get(int)

    # TODO: merge with boolean/categorical
    mini_freq_table_rows = freq_table(
        freqtable=summary["value_counts"], n=summary["n"], max_number_to_print=n_obs_cat
    )
    template_variables = render_common(summary)

    keys = ["scheme", "netloc", "path", "query", "fragment"]
    for url_part in keys:
        template_variables[f"freqtable_{url_part}"] = freq_table(
            freqtable=summary[f"{url_part}_counts"],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        )

    full_frequency_table = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Full",
        anchor_id=f"{varid}full_frequency",
    )
    scheme_frequency_table = FrequencyTable(
        template_variables["freqtable_scheme"],
        name="Scheme",
        anchor_id=f"{varid}scheme_frequency",
    )
    netloc_frequency_table = FrequencyTable(
        template_variables["freqtable_netloc"],
        name="Netloc",
        anchor_id=f"{varid}netloc_frequency",
    )
    path_frequency_table = FrequencyTable(
        template_variables["freqtable_path"],
        name="Path",
        anchor_id=f"{varid}path_frequency",
    )
    query_frequency_table = FrequencyTable(
        template_variables["freqtable_query"],
        name="Query",
        anchor_id=f"{varid}query_frequency",
    )
    fragment_frequency_table = FrequencyTable(
        template_variables["freqtable_fragment"],
        name="Fragment",
        anchor_id=f"{varid}fragment_frequency",
    )

    items = [
        full_frequency_table,
        scheme_frequency_table,
        netloc_frequency_table,
        path_frequency_table,
        query_frequency_table,
        fragment_frequency_table,
    ]
    template_variables["bottom"] = Container(
        items, sequence_type="tabs", name="url stats", anchor_id=f"{varid}urlstats"
    )

    # Element composition
    info = VariableInfo(
        summary["varid"], summary["varname"], "URL", summary["warnings"]
    )

    table = Table(
        [
            {
                "name": "Distinct count",
                "value": summary["n_unique"],
                "fmt": "fmt",
                "alert": False,
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
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
            {
                "name": "Memory size",
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
                "alert": False,
            },
        ]
    )

    fqm = FrequencyTableSmall(mini_freq_table_rows)

    template_variables["top"] = Container([info, table, fqm], sequence_type="grid")

    return template_variables
