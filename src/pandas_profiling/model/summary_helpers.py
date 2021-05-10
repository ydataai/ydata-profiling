import os
import string
from collections import Counter
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats.stats import chisquare
from tangled_up_in_unicode import block, block_abbr, category, category_long, script

from pandas_profiling.config import Settings
from pandas_profiling.model.summary_helpers_image import (
    extract_exif,
    hash_image,
    is_image_truncated,
    open_image,
)


def mad(arr: np.ndarray) -> np.ndarray:
    """Median Absolute Deviation: a "Robust" version of standard deviation.
    Indices variability of the sample.
    https://en.wikipedia.org/wiki/Median_absolute_deviation
    """
    return np.median(np.abs(arr - np.median(arr)))


def named_aggregate_summary(series: pd.Series, key: str) -> dict:
    summary = {
        f"max_{key}": np.max(series),
        f"mean_{key}": np.mean(series),
        f"median_{key}": np.median(series),
        f"min_{key}": np.min(series),
    }

    return summary


def length_summary(series: pd.Series, summary: dict = None) -> dict:
    if summary is None:
        summary = {}

    length = series.str.len()

    summary.update({"length": length})
    summary.update(named_aggregate_summary(length, "length"))

    return summary


def file_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """

    # Transform
    stats = series.map(lambda x: os.stat(x))

    def convert_datetime(x: float) -> str:
        return datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S")

    # Transform some more
    summary = {
        "file_size": stats.map(lambda x: x.st_size),
        "file_created_time": stats.map(lambda x: x.st_ctime).map(convert_datetime),
        "file_accessed_time": stats.map(lambda x: x.st_atime).map(convert_datetime),
        "file_modified_time": stats.map(lambda x: x.st_mtime).map(convert_datetime),
    }
    return summary


def path_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """

    # TODO: optimize using value counts
    summary = {
        "common_prefix": os.path.commonprefix(series.values.tolist())
        or "No common prefix",
        "stem_counts": series.map(lambda x: os.path.splitext(x)[0]).value_counts(),
        "suffix_counts": series.map(lambda x: os.path.splitext(x)[1]).value_counts(),
        "name_counts": series.map(lambda x: os.path.basename(x)).value_counts(),
        "parent_counts": series.map(lambda x: os.path.dirname(x)).value_counts(),
        "anchor_counts": series.map(lambda x: os.path.splitdrive(x)[0]).value_counts(),
    }

    summary["n_stem_unique"] = len(summary["stem_counts"])
    summary["n_suffix_unique"] = len(summary["suffix_counts"])
    summary["n_name_unique"] = len(summary["name_counts"])
    summary["n_parent_unique"] = len(summary["parent_counts"])
    summary["n_anchor_unique"] = len(summary["anchor_counts"])

    return summary


def url_summary(series: pd.Series) -> dict:
    """

    Args:
        series: series to summarize

    Returns:

    """
    summary = {
        "scheme_counts": series.map(lambda x: x.scheme).value_counts(),
        "netloc_counts": series.map(lambda x: x.netloc).value_counts(),
        "path_counts": series.map(lambda x: x.path).value_counts(),
        "query_counts": series.map(lambda x: x.query).value_counts(),
        "fragment_counts": series.map(lambda x: x.fragment).value_counts(),
    }

    return summary


def count_duplicate_hashes(image_descriptions: dict) -> int:
    """

    Args:
        image_descriptions:

    Returns:

    """
    counts = pd.Series(
        [x["hash"] for x in image_descriptions if "hash" in x]
    ).value_counts()
    return counts.sum() - len(counts)


def extract_exif_series(image_exifs: list) -> dict:
    """

    Args:
        image_exifs:

    Returns:

    """
    exif_keys = []
    exif_values: dict = {}

    for image_exif in image_exifs:
        # Extract key
        exif_keys.extend(list(image_exif.keys()))

        # Extract values per key
        for exif_key, exif_val in image_exif.items():
            if exif_key not in exif_values:
                exif_values[exif_key] = []

            exif_values[exif_key].append(exif_val)

    series = {"exif_keys": pd.Series(exif_keys, dtype=object).value_counts().to_dict()}

    for k, v in exif_values.items():
        series[k] = pd.Series(v).value_counts()

    return series


def extract_image_information(
    path: Path, exif: bool = False, hash: bool = False
) -> dict:
    """Extracts all image information per file, as opening files is slow

    Args:
        path: Path to the image
        exif: extract exif information
        hash: calculate hash (for duplicate detection)

    Returns:
        A dict containing image information
    """
    information: dict = {}
    image = open_image(path)
    information["opened"] = image is not None
    if image is not None:
        information["truncated"] = is_image_truncated(image)
        if not information["truncated"]:
            information["size"] = image.size
            if exif:
                information["exif"] = extract_exif(image)
            if hash:
                information["hash"] = hash_image(image)

    return information


def image_summary(series: pd.Series, exif: bool = False, hash: bool = False) -> dict:
    """

    Args:
        series: series to summarize
        exif: extract exif information
        hash: calculate hash (for duplicate detection)

    Returns:

    """

    image_information = series.apply(
        partial(extract_image_information, exif=exif, hash=hash)
    )
    summary = {
        "n_truncated": sum(
            [1 for x in image_information if "truncated" in x and x["truncated"]]
        ),
        "image_dimensions": pd.Series(
            [x["size"] for x in image_information if "size" in x],
            name="image_dimensions",
        ),
    }

    image_widths = summary["image_dimensions"].map(lambda x: x[0])
    summary.update(named_aggregate_summary(image_widths, "width"))
    image_heights = summary["image_dimensions"].map(lambda x: x[1])
    summary.update(named_aggregate_summary(image_heights, "height"))
    image_areas = image_widths * image_heights
    summary.update(named_aggregate_summary(image_areas, "area"))

    if hash:
        summary["n_duplicate_hash"] = count_duplicate_hashes(image_information)

    if exif:
        exif_series = extract_exif_series(
            [x["exif"] for x in image_information if "exif" in x]
        )
        summary["exif_keys_counts"] = exif_series["exif_keys"]
        summary["exif_data"] = exif_series

    return summary


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


def histogram_compute(
    config: Settings,
    finite_values: np.ndarray,
    n_unique: int,
    name: str = "histogram",
    weights: Optional[np.ndarray] = None,
) -> dict:
    stats = {}
    bins = config.plot.histogram.bins
    bins_arg = "auto" if bins == 0 else min(bins, n_unique)
    stats[name] = np.histogram(finite_values, bins=bins_arg, weights=weights)

    max_bins = config.plot.histogram.max_bins
    if bins_arg == "auto" and len(stats[name][1]) > max_bins:
        stats[name] = np.histogram(finite_values, bins=max_bins, weights=None)

    return stats


def chi_square(
    values: Optional[np.ndarray] = None, histogram: Optional[np.ndarray] = None
) -> dict:
    if histogram is None:
        histogram, _ = np.histogram(values, bins="auto")
    return dict(chisquare(histogram)._asdict())


def word_summary(series: pd.Series) -> dict:
    # TODO: preprocess (stopwords)
    # TODO: configurable lowercase/punctuation etc.
    word_lists = series.str.lower().str.split()
    words = word_lists.explode()
    words = words.str.strip(string.punctuation)
    return {"word_counts": words.value_counts()}
