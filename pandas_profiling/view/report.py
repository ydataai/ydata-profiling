"""Generate the report."""

import pandas as pd

import pandas_profiling.view.plot as plot
from pandas_profiling.view.plot import mini_histogram
from pandas_profiling.view.plot import histogram
import pandas_profiling.view.templates as templates
from pandas_profiling.config import config
from pandas_profiling.model.base import Variable
from pandas_profiling.model.messages import MessageType


def freq_table(
    freqtable, n: int, table_template, max_number_to_print: int, idx: int, nb_col=6
) -> str:
    """Render the HTML for a frequency table (value, count).

    Args:
      idx: The variable id.
      freqtable: The frequency table.
      n: The total number of values.
      table_template: The name of the template.
      max_number_to_print: The maximum number of observatios to print.
      nb_col: The number of columns in the grid. (Default value = 6)

    Returns:
        The HTML representation of the frequency table.
    """

    if max_number_to_print > n:
        max_number_to_print = n

    if max_number_to_print < len(freqtable):
        freq_other = sum(freqtable.iloc[max_number_to_print:])
        min_freq = freqtable.values[max_number_to_print]
    else:
        freq_other = 0
        min_freq = 0

    freq_missing = n - sum(freqtable)
    max_freq = max(freqtable.values[0], freq_other, freq_missing)

    # TODO: Correctly sort missing and other
    if max_freq == 0:
        raise ValueError("Empty column")

    rows = []
    for label, freq in freqtable.iloc[0:max_number_to_print].items():
        rows.append(
            {
                "label": label,
                "width": freq / max_freq,
                "count": freq,
                "percentage": float(freq) / n,
                "extra_class": "",
            }
        )

    if freq_other > min_freq:
        rows.append(
            {
                "label": "Other values ({})".format(
                    str(freqtable.count() - max_number_to_print)
                ),
                "width": freq_other / max_freq,
                "count": freq_other,
                "percentage": float(freq_other) / n,
                "extra_class": "other",
            }
        )

    if freq_missing > min_freq:
        rows.append(
            {
                "label": "(Missing)",
                "width": freq_missing / max_freq,
                "count": freq_missing,
                "percentage": float(freq_missing) / n,
                "extra_class": "missing",
            }
        )

    return templates.template(table_template).render(
        rows=rows, varid=hash(idx), nb_col=nb_col
    )


def extreme_obs_table(freqtable, number_to_print, n, ascending=True) -> str:
    """Similar to the frequency table, for extreme observations.

    Args:
      freqtable: The frequency table.
      number_to_print: The number of observations to print.
      n: The total number of observations.
      ascending: The ordering of the observations (Default value = True)

    Returns:
        The HTML rendering of the extreme observation table.
    """
    # If it's mixed between base types (str, int) convert to str. Pure "mixed" types are filtered during type
    # discovery
    if "mixed" in freqtable.index.inferred_type:
        freqtable.index = freqtable.index.astype(str)

    sorted_freqtable = freqtable.sort_index(ascending=ascending)
    obs_to_print = sorted_freqtable.iloc[:number_to_print]
    max_freq = max(obs_to_print.values)

    rows = []
    for label, freq in obs_to_print.items():
        rows.append(
            {
                "label": label,
                "width": freq / max_freq if max_freq != 0 else 0,
                "count": freq,
                "percentage": float(freq) / n,
                "extra_class": "",
            }
        )

    return templates.template("freq_table.html").render(rows=rows)


def render_overview_html(stats_object: dict) -> str:
    """Render the overview HTML.

    Args:
        stats_object: The statistics to display in the overview.

    Returns:
        The rendered HTML for the overview component of the profile.
    """
    return templates.template("overview.html").render(
        values=stats_object["table"],
        messages=stats_object["messages"],
        variables=stats_object["variables"],
        MessageType=MessageType,
    )


def render_correlations_html(stats_object: dict) -> str:
    """Render the correlations HTML.

    Args:
        stats_object: The diagrams to display in the correlation component.

    Returns:
        The rendered HTML of the correlations component of the profile.
    """
    values = {}
    active = ""
    if "pearson" in stats_object["correlations"]:
        if active == "":
            active = "pearson"
        values["pearson"] = {
            "matrix": plot.correlation_matrix(stats_object["correlations"]["pearson"]),
            "name": "Pearson's r",
        }

    if "spearman" in stats_object["correlations"]:
        if active == "":
            active = "spearman"
        values["spearman"] = {
            "matrix": plot.correlation_matrix(stats_object["correlations"]["spearman"]),
            "name": "Spearman's &rho;",
        }

    if "kendall" in stats_object["correlations"]:
        if active == "":
            active = "kendall"
        values["kendall"] = {
            "matrix": plot.correlation_matrix(stats_object["correlations"]["kendall"]),
            "name": "Kendall's &tau;",
        }

    if "phi_k" in stats_object["correlations"]:
        if active == "":
            active = "phi_k"
        values["phi_k"] = {
            "matrix": plot.correlation_matrix(
                stats_object["correlations"]["phi_k"], vmin=0
            ),
            "name": "Phik (&phi;<sub><em>k</em></sub>)",
        }

    if "cramers" in stats_object["correlations"]:
        if active == "":
            active = "cramers"
        values["cramers"] = {
            "matrix": plot.correlation_matrix(
                stats_object["correlations"]["cramers"], vmin=0
            ),
            "name": "Cramér's V (&phi;<sub><em>c</em></sub>)",
        }

    if "recoded" in stats_object["correlations"]:
        if active == "":
            active = "recoded"
        values["recoded"] = {
            "matrix": plot.correlation_matrix(
                stats_object["correlations"]["recoded"], vmin=0
            ),
            "name": "Recoded",
        }

    return templates.template("correlations.html").render(values=values, active=active)


def render_missing_html(stats_object: dict) -> str:
    """Render the missing values HTML.

    Args:
        stats_object: The diagrams with missing values.

    Returns:
        The missing values component HTML.
    """
    return templates.template("missing.html").render(values=stats_object["missing"])


def render_variables_html(stats_object: dict) -> str:
    """Render the HTML for each of the variables in the DataFrame.

    Args:
        stats_object: The statistics for each variable.

    Returns:
        The rendered HTML, where each row represents a variable.
    """
    rows_html = u""

    n_obs_unique = config["n_obs_unique"].get(int)
    n_obs_bool = config["n_obs_bool"].get(int)
    n_extreme_obs = config["n_extreme_obs"].get(int)
    n_freq_table_max = config["n_freq_table_max"].get(int)

    messages = stats_object["messages"]

    # TODO: move to for loop in template
    for idx, row in stats_object["variables"].items():
        formatted_values = row
        formatted_values.update({"varname": idx, "varid": hash(idx), "row_classes": {}})

        # TODO: obtain from messages (ignore)
        for m in messages:
            if m.column_name == idx:
                if m.message_type == MessageType.SKEWED:
                    formatted_values["row_classes"]["skewness"] = "alert"
                elif m.message_type == MessageType.HIGH_CARDINALITY:
                    # TODO: rename alert to prevent overlap with bootstrap classes
                    formatted_values["row_classes"]["distinct_count"] = "alert"
                elif m.message_type == MessageType.ZEROS:
                    formatted_values["row_classes"]["zeros"] = "alert"
                elif m.message_type == MessageType.MISSING:
                    formatted_values["row_classes"]["missing"] = "alert"

        if row["type"] in {Variable.TYPE_NUM, Variable.TYPE_DATE}:

            formatted_values["histogram"] = histogram(row["histogramdata"], row)
            formatted_values["mini_histogram"] = mini_histogram(
                row["histogramdata"], row
            )

        if row["type"] in {Variable.TYPE_CAT, Variable.TYPE_BOOL}:
            # The number of column to use in the display of the frequency table according to the category
            mini_freq_table_nb_col = {Variable.TYPE_CAT: 6, Variable.TYPE_BOOL: 3}

            formatted_values["minifreqtable"] = freq_table(
                stats_object["variables"][idx]["value_counts_without_nan"],
                stats_object["table"]["n"],
                "mini_freq_table.html",
                max_number_to_print=n_obs_bool,
                idx=idx,
                nb_col=mini_freq_table_nb_col[row["type"]],
            )

        if row["type"] in {Variable.TYPE_URL}:
            keys = ["scheme", "netloc", "path", "query", "fragment"]
            for url_part in keys:
                formatted_values["freqtable_{}".format(url_part)] = freq_table(
                    freqtable=stats_object["variables"][idx][
                        "{}_counts".format(url_part)
                    ],
                    # TODO: n - missing
                    n=stats_object["table"]["n"],
                    table_template="freq_table.html",
                    idx=idx,
                    max_number_to_print=n_freq_table_max,
                )

        if row["type"] == Variable.S_TYPE_UNIQUE:
            table = stats_object["variables"][idx][
                "value_counts_without_nan"
            ].sort_index()
            obs = table.index

            formatted_values["firstn"] = pd.DataFrame(
                list(obs[0:n_obs_unique]),
                columns=["First {} values".format(n_obs_unique)],
            ).to_html(classes="example_values", index=False)
            formatted_values["lastn"] = pd.DataFrame(
                list(obs[-n_obs_unique:]),
                columns=["Last {} values".format(n_obs_unique)],
            ).to_html(classes="example_values", index=False)

        if row["type"] not in {
            Variable.S_TYPE_UNSUPPORTED,
            Variable.S_TYPE_CORR,
            Variable.S_TYPE_CONST,
            Variable.S_TYPE_RECODED,
        }:
            formatted_values["freqtable"] = freq_table(
                freqtable=stats_object["variables"][idx]["value_counts_without_nan"],
                n=stats_object["table"]["n"],
                table_template="freq_table.html",
                idx=idx,
                max_number_to_print=n_freq_table_max,
            )

            formatted_values["firstn_expanded"] = extreme_obs_table(
                freqtable=stats_object["variables"][idx]["value_counts_without_nan"],
                number_to_print=n_extreme_obs,
                n=stats_object["table"]["n"],
                ascending=True,
            )
            formatted_values["lastn_expanded"] = extreme_obs_table(
                freqtable=stats_object["variables"][idx]["value_counts_without_nan"],
                number_to_print=n_extreme_obs,
                n=stats_object["table"]["n"],
                ascending=False,
            )
        # if row['type'] in [Variable.TYPE_NUM, Variable.TYPE_DATE]:
        # TODO: move histograms here

        rows_html += templates.template(
            "variables/row_{}.html".format(row["type"].value.lower())
        ).render(values=formatted_values)
    return rows_html


def render_sample_html(sample: dict) -> str:
    """Render the sample HTML

    Args:
        sample: A dict containing samples from the dataset to print.

    Returns:
        The HTML rendering of the samples.
    """
    formatted_samples = {}
    for key in sample:
        formatted_samples[key] = sample[key].to_html(classes="sample table-striped")
    sample_html = templates.template("sample.html").render(values=formatted_samples)
    # Previously, we only displayed the first samples.
    # sample_html = templates.template('sample.html').render(sample_table_html=sample.to_html(classes="sample"))
    return sample_html


def to_html(sample: dict, stats_object: dict) -> str:
    """Generate a HTML report from summary statistics and a given sample.

    Args:
      sample: A dict containing the samples to print.
      stats_object: Statistics to use for the overview, variables, correlations and missing values.

    Returns:
      The profile report in HTML format
    """

    if not isinstance(sample, dict):
        raise TypeError("sample must be of type dict")

    if not isinstance(stats_object, dict):
        raise TypeError(
            "stats_object must be of type dict. Did you generate this using the "
            "pandas_profiling.describe() function?"
        )

    if not {"table", "variables", "correlations"}.issubset(set(stats_object.keys())):
        raise TypeError(
            "stats_object badly formatted. Did you generate this using the pandas_profiling.describe() function?"
        )

    render_htmls = {
        "overview_html": render_overview_html(stats_object),
        "rows_html": render_variables_html(stats_object),
        "correlations_html": render_correlations_html(stats_object),
        "missing_html": render_missing_html(stats_object),
        "sample_html": render_sample_html(sample),
        "full_width": config["style"]["full_width"].get(bool),
    }

    # TODO: should be done in the template
    return templates.template("base.html").render(render_htmls)
