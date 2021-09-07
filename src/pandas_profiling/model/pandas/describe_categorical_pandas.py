import contextlib
import string
from collections import Counter
from typing import Tuple

import numpy as np
import pandas as pd

from pandas_profiling.config import Settings
from pandas_profiling.model.pandas.utils_pandas import weighted_median
from pandas_profiling.model.schema import (
    CategoricalColumnResult,
    CharacterResult,
    StringLengthResult,
    WordResult,
)
from pandas_profiling.model.summary_algorithms import (
    chi_square,
    describe_categorical_1d,
    histogram_compute,
    series_handle_nulls,
    series_hashable,
)


def get_character_counts_vc(vc: pd.Series) -> pd.Series:
    series = pd.Series(vc.index, index=vc)
    characters = series.str.split(r".?")
    characters = characters.explode()

    counts = pd.Series(characters.index, index=characters)
    counts = counts.groupby(level=0, sort=False).sum()
    counts = counts.sort_values(ascending=False)
    # FIXME: correct in split, below should be zero: print(counts.loc[''])
    counts = counts[counts.index.str.len() > 0]
    return counts


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


def unicode_summary_vc(vc: pd.Series) -> CharacterResult:
    from tangled_up_in_unicode import block, block_abbr, category, category_long, script

    result = CharacterResult()

    # Unicode Character Summaries (category and script name)
    character_counts = get_character_counts_vc(vc)

    character_counts_series = character_counts

    result.n_characters_distinct = len(character_counts_series)
    result.n_characters = np.sum(character_counts_series.values)
    result.character_counts = character_counts_series

    char_to_block = {key: block(key) for key in character_counts.keys()}
    char_to_category_short = {key: category(key) for key in character_counts.keys()}
    char_to_script = {key: script(key) for key in character_counts.keys()}

    result.category_alias_values = {
        key: category_long(value) for key, value in char_to_category_short.items()
    }
    result.block_alias_values = {
        key: block_abbr(value) for key, value in char_to_block.items()
    }

    # Retrieve original distribution
    block_alias_counts: Counter = Counter()
    per_block_char_counts: dict = {
        k: Counter() for k in result.block_alias_values.values()
    }
    for char, n_char in character_counts.items():
        block_name = result.block_alias_values[char]
        block_alias_counts[block_name] += n_char
        per_block_char_counts[block_name][char] = n_char
    result.block_alias_counts = counter_to_series(block_alias_counts)
    result.n_block_alias = len(result.block_alias_counts)
    result.block_alias_char_counts = {
        k: counter_to_series(v) for k, v in per_block_char_counts.items()
    }

    script_counts: Counter = Counter()
    per_script_char_counts: dict = {k: Counter() for k in char_to_script.values()}
    for char, n_char in character_counts.items():
        script_name = char_to_script[char]
        script_counts[script_name] += n_char
        per_script_char_counts[script_name][char] = n_char
    result.script_counts = counter_to_series(script_counts)
    result.n_scripts = len(result.script_counts)
    result.script_char_counts = {
        k: counter_to_series(v) for k, v in per_script_char_counts.items()
    }

    category_alias_counts: Counter = Counter()
    per_category_alias_char_counts: dict = {
        k: Counter() for k in result.category_alias_values.values()
    }
    for char, n_char in character_counts.items():
        category_alias_name = result.category_alias_values[char]
        category_alias_counts[category_alias_name] += n_char
        per_category_alias_char_counts[category_alias_name][char] += n_char
    result.category_alias_counts = counter_to_series(category_alias_counts)
    if len(result.category_alias_counts) > 0:
        result.category_alias_counts.index = (
            result.category_alias_counts.index.str.replace("_", " ")
        )
    result.n_category = len(result.category_alias_counts)
    result.category_alias_char_counts = {
        k: counter_to_series(v) for k, v in per_category_alias_char_counts.items()
    }

    with contextlib.suppress(AttributeError):
        result.category_alias_counts.index = (
            result.category_alias_counts.index.str.replace("_", " ")
        )

    return result


def word_summary_vc(vc: pd.Series) -> WordResult:
    # TODO: preprocess (stopwords)
    # TODO: configurable lowercase/punctuation etc.
    # TODO: remove punctuation in words

    series = pd.Series(vc.index, index=vc)
    word_lists = series.str.lower().str.split()
    words = word_lists.explode().str.strip(string.punctuation + string.whitespace)
    word_counts = pd.Series(words.index, index=words)
    # fix for pandas 1.0.5
    word_counts = word_counts[word_counts.index.notnull()]
    word_counts = word_counts.groupby(level=0, sort=False).sum()
    word_counts = word_counts.sort_values(ascending=False)

    result = WordResult()
    result.word_counts = word_counts
    return result


def length_summary_vc(vc: pd.Series) -> StringLengthResult:
    series = pd.Series(vc.index, index=vc)
    length = series.str.len()
    length_counts = pd.Series(length.index, index=length)
    length_counts = length_counts.groupby(level=0, sort=False).sum()
    length_counts = length_counts.sort_values(ascending=False)

    result = StringLengthResult()
    result.max_length = np.max(length_counts.index)
    result.mean_length = np.average(length_counts.index, weights=length_counts.values)
    result.median_length = weighted_median(
        length_counts.index.values, weights=length_counts.values
    )
    result.min_length = np.min(length_counts.index)
    result.length_histogram = length_counts
    return result


@describe_categorical_1d.register
@series_hashable
@series_handle_nulls
def pandas_describe_categorical_1d(
    config: Settings, series: pd.Series, summary: dict
) -> Tuple[Settings, pd.Series, CategoricalColumnResult]:
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
    value_counts = summary["describe_counts"].value_counts
    value_counts.index = value_counts.index.astype(str)

    result = CategoricalColumnResult()

    redact = config.vars.cat.redact
    if not redact:
        result.first_rows = series.head(5)

    chi_squared_threshold = config.vars.num.chi_squared_threshold
    if chi_squared_threshold > 0.0:
        result.chi_squared = chi_square(histogram=value_counts.values)

    if config.vars.cat.length:
        result.length = length_summary_vc(value_counts)

        r = histogram_compute(
            config,
            result.length.length_histogram.index.values,
            len(result.length.length_histogram),
            name="histogram_length",
            weights=result.length.length_histogram.values,
        )
        result.histogram_length = r["histogram_length"]

    if config.vars.cat.characters:
        result.characters = unicode_summary_vc(value_counts)

    if config.vars.cat.words:
        result.words = word_summary_vc(value_counts)

    return config, series, result
