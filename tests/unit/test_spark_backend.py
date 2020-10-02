import pytest


@pytest.mark.sparktest
def test_import_spark_session(spark_session):
    try:
        import pyspark
        from pyspark import SparkContext, SparkConf
        from pyspark.sql import SparkSession
    except ImportError:
        pytest.fail("""Could not import pyspark - is SPARK_HOME and JAVA_HOME set as variables?
                    see https://spark.apache.org/docs/latest/quick-start.html and ensure
                    that your spark instance is configured properly"""
                    )


@pytest.mark.sparktest
def test_create_spark_session(spark_session):
    try:
        from pyspark.sql import SparkSession
        assert isinstance(spark_session, SparkSession)
    except AssertionError:
        pytest.fail("""pytest spark_session was not configured properly and could not be imported
        is pytest-spark installed and configured properly?"""
                    )
