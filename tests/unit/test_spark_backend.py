import warnings

import pytest

from pandas_profiling.utils.common import (
    VERSION_WARNING,
    test_for_pyspark_pyarrow_incompatibility,
)


@pytest.mark.sparktest
def test_import_spark_session(spark_session):
    """
    Test if its possible to import spark
    """
    try:
        import pyspark
        from pyspark import SparkConf, SparkContext
        from pyspark.sql import SparkSession
    except ImportError:
        pytest.fail(
            """Could not import pyspark - is SPARK_HOME and JAVA_HOME set as variables?
                    see https://spark.apache.org/docs/latest/quick-start.html and ensure
                    that your spark instance is configured properly"""
        )


@pytest.mark.sparktest
def test_create_spark_session(spark_session):
    """
    Test if pytest-spark's spark sessions can be properly created
    """
    try:
        from pyspark.sql import SparkSession

        assert isinstance(spark_session, SparkSession)
    except AssertionError:
        pytest.fail(
            """pytest spark_session was not configured properly and could not be created
        is pytest-spark installed and configured properly?"""
        )


@pytest.mark.sparktest
def test_spark_config_check(spark_session, monkeypatch):
    """
    test_for_pyspark_pyarrow_incompatibility
    """

    # Should warn because pyarrow version >= 0.15.0 and ARROW_PRE_0_15_IPC_FORMAT not set
    monkeypatch.setattr("pyspark.__version__", "2.3.0")
    monkeypatch.setattr("pyarrow.__version__", "0.15.0")
    monkeypatch.setattr("os.environ", {})
    with pytest.warns(UserWarning):
        test_for_pyspark_pyarrow_incompatibility()

    # Should warn because pyarrow version >= 0.15.0 and ARROW_PRE_0_15_IPC_FORMAT != 1
    monkeypatch.setattr("pyspark.__version__", "2.3.0")
    monkeypatch.setattr("pyarrow.__version__", "0.15.0")
    monkeypatch.setattr("os.environ", {"ARROW_PRE_0_15_IPC_FORMAT": 0})
    with pytest.warns(UserWarning):
        test_for_pyspark_pyarrow_incompatibility()

    # Should not warn because pyarrow version >= 0.15.0 and ARROW_PRE_0_15_IPC_FORMAT != 1
    monkeypatch.setattr("pyspark.__version__", "2.3.0")
    monkeypatch.setattr("pyarrow.__version__", "0.15.0")
    monkeypatch.setattr("os.environ", {"ARROW_PRE_0_15_IPC_FORMAT": 1})
    with pytest.warns(None) as record:
        test_for_pyspark_pyarrow_incompatibility()
    assert not record

    # Should not warn because pyarrow version < 0.15.0
    monkeypatch.setattr("pyspark.__version__", "2.3.0")
    monkeypatch.setattr("pyarrow.__version__", "0.14.1")
    monkeypatch.setattr("os.environ", {})
    with pytest.warns(None) as record:
        test_for_pyspark_pyarrow_incompatibility()
    assert not record

    # Should not warn because spark version != 2.3 or 2.4 and ARROW_PRE_0_15_IPC_FORMAT != 1
    monkeypatch.setattr("pyspark.__version__", "3.0.0")
    monkeypatch.setattr("pyarrow.__version__", "1.0.0")
    monkeypatch.setattr("os.environ", {})
    with pytest.warns(None) as record:
        test_for_pyspark_pyarrow_incompatibility()
    assert not record
