import pandas as pd
import pytest
from pandas_profiling.config import Settings
from pandas_profiling.model.describe import describe
from pandas_profiling.model.model import ModelData


@pytest.fixture()
def test_dataframe() -> pd.DataFrame:
    data = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    return data


def test_describe_with_model(test_dataframe: pd.DataFrame, summarizer, typeset):
    config = Settings()
    config.report.model_module = True
    config.target.col_name = "Survived"
    description = describe(config, test_dataframe, summarizer, typeset)
    assert description.transformations is None

    assert description.model is not None
    assert isinstance(description.model.default_model, ModelData)
    assert description.model.transformed_model is None


def test_describe_with_transforms(test_dataframe: pd.DataFrame, summarizer, typeset):
    config = Settings()
    config.report.transform_module = True
    config.target.col_name = "Survived"
    description = describe(config, test_dataframe, summarizer, typeset)
    assert description.model is None

    assert description.transformations is not None


def test_describe_with_model_and_transforms(
    test_dataframe: pd.DataFrame, summarizer, typeset
):
    config = Settings()
    config.report.model_module = True
    config.report.transform_module = True
    config.target.col_name = "Survived"
    description = describe(config, test_dataframe, summarizer, typeset)
    assert description.model is not None
    assert description.transformations is not None
