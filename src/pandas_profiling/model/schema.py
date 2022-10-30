"""Defines the data model for profile results"""
from enum import Enum
from typing import Any, Dict, Optional, TypeVar

import pandas as pd
from pydantic import BaseModel

T = TypeVar("T")  # type: ignore


class Monotonicity(Enum):
    INCREASING_STRICT = 2
    INCREASING = 1
    NOT_MONOTONIC = 0
    DECREASING = -1
    DECREASING_STRICT = -2


class ColumnResult(BaseModel):
    class Config:
        arbitrary_types_allowed = True


class GenericColumnResult(ColumnResult):
    n: Optional[int] = None
    count: Optional[int] = None
    p_missing: Optional[float] = None
    memory_size: Optional[float] = None


class BooleanColumnResult(ColumnResult):
    top: Optional[Any] = None
    freq: Optional[int] = None


class NumericColumnResult(ColumnResult):
    n_infinite: Optional[int] = None
    p_infinite: Optional[float] = None
    n_zeros: Optional[int] = None
    p_zeros: Optional[float] = None
    n_negative: Optional[int] = None
    p_negative: Optional[float] = None
    monotonic: Optional[Monotonicity] = None
    quantiles: Optional[dict] = None
    mad: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    variance: Optional[float] = None
    kurtosis: Optional[float] = None
    skewness: Optional[float] = None
    sum: Optional[float] = None
    range: Optional[float] = None
    iqr: Optional[float] = None
    cv: Optional[float] = None
    chi_squared: Optional[Any] = None
    histogram: Optional[Any] = None


class CountColumnResult(ColumnResult):
    hashable: Optional[bool] = None
    n_missing: Optional[int] = None
    value_counts: Optional[pd.Series] = None
    values: Optional[pd.Series] = None


class SupportedColumnResult(ColumnResult):
    n_distinct: Optional[int] = None
    n_unique: Optional[int] = None
    p_distinct: Optional[float] = None
    is_unique: Optional[bool] = None
    p_unique: Optional[float] = None


class WordResult(BaseModel):
    word_counts: Optional[pd.Series] = None

    class Config:
        arbitrary_types_allowed = True


class CharacterResult(BaseModel):
    n_characters_distinct: Optional[int]
    n_characters: Optional[int]
    n_block_alias: Optional[int]
    n_scripts: Optional[int]
    n_category: Optional[int]
    character_counts: Optional[pd.Series]
    character_alias_values: Optional[pd.Series]
    block_alias_values: Optional[pd.Series]
    block_alias_char_counts: Optional[dict]
    block_alias_counts: Optional[pd.Series]
    category_alias_counts: Optional[pd.Series]
    script_counts: Optional[pd.Series]
    script_char_counts: Optional[pd.Series]
    category_alias_values: Optional[pd.Series]
    category_alias_char_counts: Optional[pd.Series]

    class Config:
        arbitrary_types_allowed = True


class StringLengthResult(BaseModel):
    max_length: Optional[int] = None
    mean_length: Optional[float] = None
    median_length: Optional[int] = None
    min_length: Optional[int] = None
    length_histogram: Optional[pd.Series] = None

    class Config:
        arbitrary_types_allowed = True


class CategoricalColumnResult(ColumnResult):
    first_rows: Optional[pd.DataFrame] = None
    chi_squared: Optional[Any] = None
    characters: Optional[CharacterResult] = None
    words: Optional[WordResult] = None
    length: Optional[StringLengthResult] = None
    histogram_length: Optional[Any]


class UrlColumnResult(ColumnResult):
    scheme_counts: Optional[pd.Series] = None
    netloc_counts: Optional[pd.Series] = None
    path_counts: Optional[pd.Series] = None
    query_counts: Optional[pd.Series] = None
    fragment_counts: Optional[pd.Series] = None


class FileColumnResult(ColumnResult):
    file_size: Optional[pd.Series] = None
    file_created_time: Optional[pd.Series] = None
    file_accessed_time: Optional[pd.Series] = None
    file_modified_time: Optional[pd.Series] = None
    histogram_file_size: Optional[Any] = None


class PathColumnResult(ColumnResult):
    common_prefix: Optional[str] = None
    stem_counts: Optional[pd.Series] = None
    suffix_counts: Optional[pd.Series] = None
    name_counts: Optional[pd.Series] = None
    parent_counts: Optional[pd.Series] = None
    anchor_counts: Optional[pd.Series] = None
    n_stem_unique: Optional[int] = None
    n_suffix_unique: Optional[int] = None
    n_name_unique: Optional[int] = None
    n_parent_unique: Optional[int] = None
    n_anchor_unique: Optional[int] = None


class DateColumnResult(ColumnResult):
    min: Optional[int] = None
    max: Optional[int] = None
    range: Optional[float] = None
    chi_squared: Optional[Any] = None
    histogram: Optional[Any] = None


class ImageColumnResult(ColumnResult):
    n_duplicate_hash: Optional[int] = None
    n_truncated: Optional[int] = None
    image_dimensions: Optional[pd.Series] = None
    min_width: Optional[int]
    max_width: Optional[int]
    mean_width: Optional[float]
    median_width: Optional[int]
    min_height: Optional[int]
    max_height: Optional[int]
    mean_height: Optional[float]
    median_height: Optional[int]
    min_area: Optional[int]
    max_area: Optional[int]
    mean_area: Optional[float]
    median_area: Optional[int]
    exif_keys_counts: Optional[Any]
    exif_data: Optional[Any]


class DuplicateResult(BaseModel):
    n_duplicates: Optional[int]
    p_duplicates: Optional[float]


class TableResult(BaseModel):
    n: Optional[int] = None
    n_var: Optional[int] = None
    memory_size: Optional[int] = None
    record_size: Optional[int] = None
    n_cells_missing: Optional[int] = None
    p_cells_missing: Optional[float] = None
    n_vars_with_missing: Optional[int] = None
    n_vars_all_missing: Optional[int] = None
    types: Optional[Dict[str, int]] = None
    duplicates: Optional[DuplicateResult]


class ProfileResult(BaseModel):
    table = TableResult()
    variables = Dict[str, ColumnResult]

    class Config:
        arbitrary_types_allowed = True


class Sample(BaseModel):
    id: str
    data: pd.DataFrame
    name: str
    caption: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
