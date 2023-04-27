from __future__ import annotations

import pandas as pd
from lightgbm import LGBMClassifier
from pandas_profiling.config import Settings
from pandas_profiling.model.data import ConfMatrixData
from pandas_profiling.model.description_target import TargetDescription
from pandas_profiling.model.model import (
    Model,
    ModelData,
    ModelEvaluation,
    ModelModule,
    get_model_module,
)
from pandas_profiling.model.transformations import get_train_test_split
from sklearn import metrics
from sklearn.model_selection import train_test_split


class ModelPandas(Model):
    model: LGBMClassifier

    def __init__(self, seed: int) -> None:
        self.model = LGBMClassifier(
            max_depth=3,
            n_estimators=10,
            num_leaves=10,
            subsample_for_bin=None,
            random_state=seed,
        )

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        self.model.fit(X, y)

    def transform(self, X: pd.DataFrame):
        return self.model.predict(X)


class ModelDataPandas(ModelData):
    model: ModelPandas
    X_train: pd.DataFrame
    X_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    model_name: str = "Gradient Boosting Decision Tree"

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
        self.model = ModelPandas(config.model_seed)
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

    @classmethod
    def get_model_from_df(
        cls,
        config: Settings,
        target_description: TargetDescription,
        df: pd.DataFrame,
    ) -> ModelDataPandas:
        X_train, X_test, y_train, y_test = get_train_test_split(
            config.model_seed, df, target_description
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
    object_cols = df.select_dtypes(include=["object"]).columns
    df[object_cols] = df[object_cols].astype("category")
    return ModelModulePandas(config, target_description, df)
