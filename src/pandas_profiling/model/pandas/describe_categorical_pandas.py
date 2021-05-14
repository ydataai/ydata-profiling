import contextlib
import string
from collections import Counter
from typing import Tuple

import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_algorithms import (
    chi_square,
    describe_categorical_1d,
    histogram_compute,
    named_aggregate_summary,
    series_handle_nulls,
    series_hashable,
)


def get_character_counts(series: pd.Series) -> Counter:
    """Function to return the character counts

    Args:
        series: the Series to process

    Returns:
        A dict with character counts
    """
    return Counter(series.str.cat())


def counter_to_series(counter: Counter) -> pd.Series:
    if not counter:
        return pd.Series([], dtype=object)

    counter_as_tuples = counter.most_common()
    items, counts = zip(*counter_as_tuples)
    return pd.Series(counts, index=items)


def unicode_summary(series: pd.Series) -> dict:
    from tangled_up_in_unicode import block, block_abbr, category, category_long, script

    # Unicode Character Summaries (category and script name)
    character_counts = get_character_counts(series)

    character_counts_series = counter_to_series(character_counts)

    char_to_block = {key: block(key) for key in character_counts.keys()}
    char_to_category_short = {key: category(key) for key in character_counts.keys()}
    char_to_script = {key: script(key) for key in character_counts.keys()}

    summary = {
        "n_characters": len(character_counts_series),
        "character_counts": character_counts_series,
        "category_alias_values": {
            key: category_long(value) for key, value in char_to_category_short.items()
        },
        "block_alias_values": {
            key: block_abbr(value) for key, value in char_to_block.items()
        },
    }
    # Retrieve original distribution
    block_alias_counts: Counter = Counter()
    per_block_char_counts: dict = {
        k: Counter() for k in summary["block_alias_values"].values()
    }
    for char, n_char in character_counts.items():
        block_name = summary["block_alias_values"][char]
        block_alias_counts[block_name] += n_char
        per_block_char_counts[block_name][char] = n_char
    summary["block_alias_counts"] = counter_to_series(block_alias_counts)
    summary["block_alias_char_counts"] = {
        k: counter_to_series(v) for k, v in per_block_char_counts.items()
    }

    script_counts: Counter = Counter()
    per_script_char_counts: dict = {k: Counter() for k in char_to_script.values()}
    for char, n_char in character_counts.items():
        script_name = char_to_script[char]
        script_counts[script_name] += n_char
        per_script_char_counts[script_name][char] = n_char
    summary["script_counts"] = counter_to_series(script_counts)
    summary["script_char_counts"] = {
        k: counter_to_series(v) for k, v in per_script_char_counts.items()
    }

    category_alias_counts: Counter = Counter()
    per_category_alias_char_counts: dict = {
        k: Counter() for k in summary["category_alias_values"].values()
    }
    for char, n_char in character_counts.items():
        category_alias_name = summary["category_alias_values"][char]
        category_alias_counts[category_alias_name] += n_char
        per_category_alias_char_counts[category_alias_name][char] += n_char
    summary["category_alias_counts"] = counter_to_series(category_alias_counts)
    summary["category_alias_char_counts"] = {
        k: counter_to_series(v) for k, v in per_category_alias_char_counts.items()
    }

    # Unique counts
    summary["n_category"] = len(summary["category_alias_counts"])
    summary["n_scripts"] = len(summary["script_counts"])
    summary["n_block_alias"] = len(summary["block_alias_counts"])
    if len(summary["category_alias_counts"]) > 0:
        summary["category_alias_counts"].index = summary[
            "category_alias_counts"
        ].index.str.replace("_", " ")

    return summary


def word_summary(series: pd.Series) -> dict:
    # TODO: preprocess (stopwords)
    # TODO: configurable lowercase/punctuation etc.
    word_lists = series.str.lower().str.split()
    words = word_lists.explode()
    words = words.str.strip(string.punctuation)
    return {"word_counts": words.value_counts()}


def length_summary(series: pd.Series, summary: dict = None) -> dict:
    if summary is None:
        summary = {}

    length = series.str.len()

    summary.update({"length": length})
    summary.update(named_aggregate_summary(length, "length"))

    return summary


@describe_categorical_1d.register
@series_hashable
@series_handle_nulls
def pandas_describe_categorical_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, dict]:
    """Describe a categorical series.

    Args:
        config: report Settings object
        series: The Series to describe.
        summary: The dict containing the series description so far.

    Returns:
        A dict containing calculated series description values.
    """

    # Make sure we deal with strings (Issue #100)
    series = series.astype(str)

    # Only run if at least 1 non-missing value
    value_counts = summary["value_counts_without_nan"]
    histogram_largest = config.vars.cat.histogram_largest
    histogram_data = value_counts
    if histogram_largest > 0:
        histogram_data = histogram_data.nlargest(histogram_largest)

    summary.update(
        histogram_compute(
            config,
            histogram_data,
            summary["n_distinct"],
            name="histogram_frequencies",
        )
    )

    redact = config.vars.cat.redact
    if not redact:
        summary.update({"first_rows": series.head(5)})

    chi_squared_threshold = config.vars.num.chi_squared_threshold
    if chi_squared_threshold > 0.0:
        summary["chi_squared"] = chi_square(histogram=value_counts.values)

    if config.vars.cat.length:
        summary.update(length_summary(series))
        summary.update(
            histogram_compute(
                config,
                summary["length"],
                summary["length"].nunique(),
                name="histogram_length",
            )
        )

    if config.vars.cat.characters:
        summary.update(unicode_summary(series))
        summary["n_characters_distinct"] = summary["n_characters"]
        summary["n_characters"] = summary["character_counts"].values.sum()

        with contextlib.suppress(AttributeError):
            summary["category_alias_counts"].index = summary[
                "category_alias_counts"
            ].index.str.replace("_", " ")

    if config.vars.cat.words:
        summary.update(word_summary(series))

    return config, series, summary
