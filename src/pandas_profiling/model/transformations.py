from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from multimethod import multimethod

from pandas_profiling.config import Settings
from pandas_profiling.model.description_target import TargetDescription
from pandas_profiling.model.model import ModelData, get_train_test_split


@dataclass
class TransformationData:
    col_name: str
    X_train: Any
    X_test: Any
    y_train: Any
    y_test: Any
    transform_name: str
    transform_desc: str
    model_data: ModelData

    def get_better(self, other: TransformationData) -> TransformationData:
        model_evaluation = self.model_data.evaluate()
        model_evaluation_other = other.model_data.evaluate()
        if model_evaluation.quality > model_evaluation_other.quality:
            return self
        return other


class Transformation:
    transformer: Any
    transformation_name: str
    transformation_description: str
    seed: int

    def __init__(self, seed) -> None:
        self.seed = seed

    @multimethod
    def fit(self, X: Any):
        raise NotImplementedError

    @multimethod
    def transform(self, X: Any) -> Any:
        raise NotImplementedError

    def supports_nan(self) -> bool:
        return True


class NormalizeTransformation(Transformation):
    transformation_name: str = "Normalize"
    transformation_description: str = (
        "Standardize features by removing the mean and scaling to unit variance."
    )


class BinningTransformation(Transformation):
    transformation_name: str = "Binning"
    transformation_description: str = (
        "Bin continuous data into intervals with equal frequency."
    )

    def supports_nan(self) -> bool:
        return False


class OneHotTransformation(Transformation):
    transformation_name: str = "One Hot Encoding"
    transformation_description: str = (
        "Encode categorical features as a one-hot numeric array."
    )


class TfIdfTransformation(Transformation):
    transformation_name: str = "TfIdf"
    transformation_description: str = (
        "Convert a collection of raw documents to a matrix of TF-IDF features."
    )
    significant_words: List[str]

    def supports_nan(self) -> bool:
        return False


@multimethod
def get_best_transformation(
    config: Settings,
    X_train: Any,
    X_test: Any,
    y_train: Any,
    y_test: Any,
    col_name: str,
    transformations: List[Callable],
) -> TransformationData:
    raise NotImplementedError


def get_transformations_map() -> Dict[str, List[Any]]:
    """Get valid transformations for column type.

    Returns:
        Dict[List[Callable]]: Valid transformations
    """
    return {
        "Numeric": [
            NormalizeTransformation,
            BinningTransformation,
        ],
        "Text": [
            TfIdfTransformation,
        ],
        "Categorical": [
            OneHotTransformation,
        ],
    }


def get_transformations_module(
    config: Settings,
    variables_desc: Dict[str, Any],
    target_desc: TargetDescription,
    df: Any,
    base_model: Optional[ModelData],
) -> List[TransformationData]:
    transformations = []
    transform_map = get_transformations_map()
    X_train, X_test, y_train, y_test = get_train_test_split(
        config.model.model_seed, df, target_desc, config.model.test_size
    )
    for var_name, var_desc in variables_desc.items():
        var_type = var_desc["type"]
        if var_type in transform_map:
            best_transformation: Optional[TransformationData] = get_best_transformation(
                config,
                X_train,
                X_test,
                y_train,
                y_test,
                var_name,
                transform_map[var_type],
            )
            if best_transformation is not None:
                if (
                    base_model is not None
                    and base_model.evaluate().quality
                    >= best_transformation.model_data.evaluate().quality
                ):
                    continue
                transformations.append(best_transformation)

    return transformations
