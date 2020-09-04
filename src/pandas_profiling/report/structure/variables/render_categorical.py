from pandas_profiling.config import config
from pandas_profiling.report.formatters import help
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    FrequencyTableSmall,
    Image,
    Table,
    VariableInfo,
)
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.visualisation.plot import histogram, pie_plot


def render_categorical_frequency(summary, varid, image_format):
    frequency_table = Table(
        [
            {
                "name": "Unique",
                "value": f"{summary['n_unique']} {help('The number of unique values (all values that occur exactly once in the dataset).')}",
                "fmt": "raw",
                "alert": "n_unique" in summary["warn_fields"],
            },
            {
                "name": "Unique (%)",
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "alert": "p_unique" in summary["warn_fields"],
            },
        ],
        name="Unique",
        anchor_id=f"{varid}_unique_stats",
    )

    frequencies = Image(
        histogram(*summary["histogram_frequencies"]),
        image_format=image_format,
        alt="frequencies histogram",
        name="Frequencies histogram",
        caption="Frequencies of value counts",
        anchor_id=f"{varid}frequencies",
    )

    return frequency_table, frequencies


def render_categorical_length(summary, varid, image_format):
    length_table = Table(
        [
            {
                "name": "Max length",
                "value": summary["max_length"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Median length",
                "value": summary["median_length"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Mean length",
                "value": summary["mean_length"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Min length",
                "value": summary["min_length"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
        ],
        name="Length",
        anchor_id=f"{varid}lengthstats",
    )

    length_histo = Image(
        histogram(*summary["histogram_length"]),
        image_format=image_format,
        alt="length histogram",
        name="Length",
        caption="Histogram of lengths of the category",
        anchor_id=f"{varid}length",
    )

    return length_table, length_histo


def render_categorical_unicode(summary, varid, redact):
    n_freq_table_max = config["n_freq_table_max"].get(int)

    category_overview = FrequencyTable(
        freq_table(
            freqtable=summary["category_alias_counts"],
            n=summary["category_alias_counts"].sum(),
            max_number_to_print=n_freq_table_max,
        ),
        name="Most occurring categories",
        anchor_id=f"{varid}category_long_values",
        redact=False,
    )

    cats = []
    for category_alias_name, category_alias_counts in sorted(
        summary["category_alias_char_counts"].items(), key=lambda x: -len(x[1])
    ):
        category_alias_name = category_alias_name.replace("_", " ")
        cats.append(
            FrequencyTable(
                freq_table(
                    freqtable=category_alias_counts,
                    n=category_alias_counts.sum(),
                    max_number_to_print=n_freq_table_max,
                ),
                name=f"{category_alias_name}",
                anchor_id=f"{varid}category_alias_values_{category_alias_name}",
                redact=redact,
            )
        )

    category_items = [
        category_overview,
        Container(
            cats,
            name="Most frequent character per category",
            sequence_type="batch_grid",
            anchor_id=f"{varid}categories",
            batch_size=3,
        ),
    ]

    script_overview = FrequencyTable(
        freq_table(
            freqtable=summary["script_counts"],
            n=summary["script_counts"].sum(),
            max_number_to_print=n_freq_table_max,
        ),
        name="Most occurring scripts",
        anchor_id=f"{varid}script_values",
        redact=False,
    )

    scripts = []
    for script_name, script_counts in sorted(
        summary["script_char_counts"].items(), key=lambda x: -len(x[1])
    ):
        scripts.append(
            FrequencyTable(
                freq_table(
                    freqtable=script_counts,
                    n=script_counts.sum(),
                    max_number_to_print=n_freq_table_max,
                ),
                name=f"{script_name}",
                anchor_id=f"{varid}script_values_{script_name}",
                redact=redact,
            )
        )

    script_items = [
        script_overview,
        Container(
            scripts,
            name="Most frequent character per script",
            sequence_type="batch_grid",
            anchor_id=f"{varid}scripts",
            batch_size=3,
        ),
    ]

    block_overview = FrequencyTable(
        freq_table(
            freqtable=summary["block_alias_counts"],
            n=summary["block_alias_counts"].sum(),
            max_number_to_print=n_freq_table_max,
        ),
        name="Most occurring blocks",
        anchor_id=f"{varid}block_alias_values",
        redact=False,
    )

    blocks = []
    for block_name, block_counts in summary["block_alias_char_counts"].items():
        blocks.append(
            FrequencyTable(
                freq_table(
                    freqtable=block_counts,
                    n=block_counts.sum(),
                    max_number_to_print=n_freq_table_max,
                ),
                name=f"{block_name}",
                anchor_id=f"{varid}block_alias_values_{block_name}",
                redact=redact,
            )
        )

    block_items = [
        block_overview,
        Container(
            blocks,
            name="Most frequent character per block",
            sequence_type="batch_grid",
            anchor_id=f"{varid}blocks",
            batch_size=3,
        ),
    ]

    overview_table = Table(
        [
            {
                "name": "Total characters",
                "value": summary["n_characters"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Distinct characters",
                "value": summary["n_characters_distinct"],
                "fmt": "fmt_numeric",
                "alert": False,
            },
            {
                "name": "Distinct categories",
                "value": f"{summary['n_category']} {help(title='Unicode categories (click for more information)', url='https://en.wikipedia.org/wiki/Unicode_character_property#General_Category')}",
                "fmt": "raw",
                "alert": False,
            },
            {
                "name": "Distinct scripts",
                "value": f"{summary['n_scripts']} {help(title='Unicode scripts (click for more information)', url='https://en.wikipedia.org/wiki/Script_(Unicode)#List_of_scripts_in_Unicode')}",
                "fmt": "raw",
                "alert": False,
            },
            {
                "name": "Distinct blocks",
                "value": f"{summary['n_block_alias']} {help(title='Unicode blocks (click for more information)', url='https://en.wikipedia.org/wiki/Unicode_block')}",
                "fmt": "raw",
                "alert": False,
            },
        ],
        name="Characters and Unicode",
        caption="The Unicode Standard assigns character properties to each code point, which can be used to analyse textual variables. ",
    )

    citems = [
        Container(
            [
                FrequencyTable(
                    freq_table(
                        freqtable=summary["character_counts"],
                        n=summary["character_counts"].sum(),
                        max_number_to_print=n_freq_table_max,
                    ),
                    name="Most occurring characters",
                    anchor_id=f"{varid}character_frequency",
                    redact=redact,
                ),
            ],
            name="Characters",
            anchor_id=f"{varid}characters",
            sequence_type="named_list",
        ),
        Container(
            category_items,
            name="Categories",
            anchor_id=f"{varid}categories",
            sequence_type="named_list",
        ),
        Container(
            script_items,
            name="Scripts",
            anchor_id=f"{varid}scripts",
            sequence_type="named_list",
        ),
        Container(
            block_items,
            name="Blocks",
            anchor_id=f"{varid}blocks",
            sequence_type="named_list",
        ),
    ]

    return overview_table, Container(
        citems,
        name="Unicode",
        sequence_type="tabs",
        anchor_id=f"{varid}unicode",
    )


def render_categorical(summary):
    varid = summary["varid"]
    n_obs_cat = config["vars"]["cat"]["n_obs"].get(int)
    image_format = config["plot"]["image_format"].get(str)
    redact = config["vars"]["cat"]["redact"].get(bool)
    words = config["vars"]["cat"]["words"].get(bool)
    characters = config["vars"]["cat"]["characters"].get(bool)
    length = config["vars"]["cat"]["length"].get(bool)

    template_variables = render_common(summary)

    info = VariableInfo(
        summary["varid"],
        summary["varname"],
        "Categorical",
        summary["warnings"],
        summary["description"],
    )

    table = Table(
        [
            {
                "name": "Distinct",
                "value": summary["n_distinct"],
                "fmt": "fmt",
                "alert": "n_distinct" in summary["warn_fields"],
            },
            {
                "name": "Distinct (%)",
                "value": summary["p_distinct"],
                "fmt": "fmt_percent",
                "alert": "p_distinct" in summary["warn_fields"],
            },
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

    fqm = FrequencyTableSmall(
        freq_table(
            freqtable=summary["value_counts_without_nan"],
            n=summary["count"],
            max_number_to_print=n_obs_cat,
        ),
        redact=redact,
    )

    template_variables["top"] = Container([info, table, fqm], sequence_type="grid")

    # ============================================================================================

    frequency_table = FrequencyTable(
        template_variables["freq_table_rows"],
        name="Common Values",
        anchor_id=f"{varid}common_values",
        redact=redact,
    )

    unique_stats, value_counts = render_categorical_frequency(
        summary, varid, image_format
    )

    overview_items = []

    if length:
        length_table, length_histo = render_categorical_length(
            summary, varid, image_format
        )
        overview_items.append(length_table)

    if characters:
        overview_table_char, unitab = render_categorical_unicode(summary, varid, redact)
        overview_items.append(overview_table_char)

    overview_items.append(unique_stats)

    if not redact:
        rows = ("1st row", "2nd row", "3rd row", "4th row", "5th row")

        sample = Table(
            [
                {
                    "name": name,
                    "value": value,
                    "fmt": "fmt",
                    "alert": False,
                }
                for name, value in zip(rows, summary["first_rows"])
            ],
            name="Sample",
        )
        overview_items.append(sample)

    string_items = [frequency_table]
    if length:
        string_items.append(length_histo)

    max_unique = config["plot"]["pie"]["max_unique"].get(int)
    if max_unique > 0 and summary["n_distinct"] <= max_unique:
        string_items.append(
            Image(
                pie_plot(
                    summary["value_counts_without_nan"],
                    legend_kws={"loc": "upper right"},
                ),
                image_format=image_format,
                alt="Pie chart",
                name="Pie chart",
                anchor_id=f"{varid}pie_chart",
            )
        )

    bottom_items = [
        Container(
            overview_items,
            name="Overview",
            anchor_id=f"{varid}overview",
            sequence_type="batch_grid",
            batch_size=len(overview_items),
            titles=False,
        ),
        Container(
            string_items,
            name="Categories",
            anchor_id=f"{varid}string",
            sequence_type="batch_grid",
            batch_size=len(string_items),
        ),
    ]

    if words:
        woc = freq_table(
            freqtable=summary["word_counts"],
            n=summary["word_counts"].sum(),
            max_number_to_print=10,
        )

        fqwo = FrequencyTable(
            woc,
            name="Common words",
            anchor_id=f"{varid}cwo",
            redact=redact,
        )

        bottom_items.append(
            Container(
                [fqwo],
                name="Words",
                anchor_id=f"{varid}word",
                sequence_type="grid",
            )
        )

    if characters:
        bottom_items.append(
            Container(
                [unitab],
                name="Characters",
                anchor_id=f"{varid}characters",
                sequence_type="grid",
            )
        )

    # Bottom
    template_variables["bottom"] = Container(
        bottom_items, sequence_type="tabs", anchor_id=f"{varid}bottom"
    )

    return template_variables
