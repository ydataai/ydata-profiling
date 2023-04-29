from __future__ import annotations

from typing import List, Tuple

import pandas as pd
from lightgbm import LGBMClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split

from pandas_profiling.config import Model as ModelConfig
from pandas_profiling.config import Settings
from pandas_profiling.model.data import ConfMatrixData
from pandas_profiling.model.description_target import TargetDescription
from pandas_profiling.model.model import (
    Model,
    ModelData,
    ModelEvaluation,
    ModelModule,
    get_model_module,
    get_train_test_split,
)


@get_train_test_split.register
def get_train_test_split_pandas(
    seed: int, df: pd.DataFrame, target_description: TargetDescription, test_size: float
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = df.drop(columns=target_description.name)
    y = target_description.series_binary
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=seed
    )
    return X_train, X_test, y_train, y_test


class ModelPandas(Model):
    model: LGBMClassifier

    def __init__(self, model_config: ModelConfig) -> None:
        self.model = LGBMClassifier(
            max_depth=model_config.max_depth,
            n_estimators=model_config.n_estimators,
            num_leaves=model_config.num_leaves,
            random_state=model_config.model_seed,
            importance_type="gain",
        )

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        X = X.select_dtypes(exclude=["object"])
        self.model.fit(X, y)

    def transform(self, X: pd.DataFrame):
        X = X.select_dtypes(exclude=["object"])
        return self.model.predict(X)


class ModelDataPandas(ModelData):
    model: ModelPandas
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    train_test_split_policy: str = "random"
    boosting_type: str = "Gradient Boosting Decision Tree"
    model_source: str = "lightgbm.LGBMClassifier"

    def __init__(
        self,
        config: Settings,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> None:
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        self.train_records = X_train.shape[0]
        self.test_records = X_test.shape[0]
        self.model = ModelPandas(config.model)
        self.model.fit(X_train, y_train)
        self.y_pred = self.model.transform(X_test)

    def evaluate(self) -> ModelEvaluation:
        precision = metrics.precision_score(self.y_pred, self.y_test)
        recall = metrics.recall_score(self.y_pred, self.y_test)
        f1 = metrics.f1_score(self.y_pred, self.y_test)
        accuracy = metrics.accuracy_score(self.y_pred, self.y_test)

        # conf_matrix = metrics.confusion_matrix(self.y_pred, self.y_test)
        conf_matrix = pd.crosstab(
            self.y_test,
            self.y_pred,
            rownames=["Actual value"],
            colnames=["Predicted value"],
        )
        conf_matrix_relative = pd.crosstab(
            self.y_test,
            self.y_pred,
            rownames=["Actual value"],
            colnames=["Predicted value"],
            normalize="index",
        )
        conf_matrix = ConfMatrixData(conf_matrix, conf_matrix_relative)

        return ModelEvaluation(
            accuracy=float(accuracy),
            precision=float(precision),
            recall=float(recall),
            f1_score=float(f1),
            confusion_matrix=conf_matrix,
        )

    def get_feature_importances(self) -> List[Tuple[float, str]]:
        importances = self.model.model.feature_importances_
        names = self.model.model.feature_name_
        importance_feature = list(zip(importances, names))
        importance_feature.sort(key=lambda x: x[0], reverse=True)
        return importance_feature

    @classmethod
    def get_model_from_df(
        cls,
        config: Settings,
        target_description: TargetDescription,
        df: pd.DataFrame,
    ) -> ModelDataPandas:
        X_train, X_test, y_train, y_test = get_train_test_split(
            config.model.model_seed, df, target_description, config.model.test_size
        )
        return ModelDataPandas(config, X_train, X_test, y_train, y_test)


class ModelModulePandas(ModelModule):
    def __init__(
        self,
        config: Settings,
        target_description: TargetDescription,
        df: pd.DataFrame,
    ):
        self.default_model = ModelDataPandas.get_model_from_df(
            config, target_description, df
        )
        self.transformed_model = None


@get_model_module.register
def get_model_module_pandas(
    config: Settings,
    target_description: TargetDescription,
    df: pd.DataFrame,
) -> ModelModule:
    return ModelModulePandas(config, target_description, df)
