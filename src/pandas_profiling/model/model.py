from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

import pandas as pd
from multimethod import multimethod
from pandas_profiling.config import Settings
from pandas_profiling.model.description_target import TargetDescription
from pandas_profiling.model.missing import MissingConfMatrix


@dataclass
class ModelEvaluation:
    """Class for data from model evaluations."""

    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: MissingConfMatrix

    @property
    def quality(self) -> float:
        return self.accuracy + self.precision + self.recall + self.f1_score


class Model(ABC):
    """Abstract class for models."""

    @abstractmethod
    def __init__(self) -> None:
        """Model creation."""

    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def transform(self, X):
        pass


class ModelData:
    X_train: Any
    X_test: Any
    y_train: Any
    y_test: Any

    train_records: int
    test_records: int
    n_of_features: int

    model_name: str

    @abstractmethod
    def evaluate(self) -> ModelEvaluation:
        """Evaluate model.

        Returns:
            ModelEvaluation: evaluation of model
        """


@dataclass
class ModelModule:
    default_model: ModelData
    transformed_model: Optional[ModelData]


@multimethod
def get_model_module(
    config: Settings, target_description: TargetDescription, df: Any
) -> ModelModule:
    raise NotImplementedError()
