import pytest

from pandas_profiling.model.correlations import *


@pytest.fixture
def correlation_data():
    correlation_testdata = pd.DataFrame(
        {
            "test_num_1": [1, 2, 3, 5, 7, 8, 9],
            "test_num_2": [11, 12, 13, 15, 17, 18, 4],
            "test_cat_1": ["one", "one", "one", "two", "two", "four", "four"],
            "test_cat_2": ["one", "one", "two", "two", "three", "four", "four"],
        }
    )

    test_descriptions_spark = {
        "test_num_1": {"n_distinct": 7, "type": SparkNumeric},
        "test_num_2": {"n_distinct": 7, "type": SparkNumeric},
        "test_cat_1": {"n_distinct": 3, "type": SparkCategorical},
        "test_cat_2": {"n_distinct": 4, "type": SparkCategorical},
    }

    return {"data": correlation_testdata, "descriptions": test_descriptions_spark}


@pytest.fixture
def expected_results():
    expected_results = {
        "pearson": {
            "test_num_1": {"test_num_1": 1.0, "test_num_2": -0.022957113535640776},
            "test_num_2": {"test_num_1": -0.022957113535640776, "test_num_2": 1.0},
        },
        "spearman": {
            "test_num_1": {"test_num_1": 1.0, "test_num_2": 0.25000000000000017},
            "test_num_2": {"test_num_1": 0.25000000000000017, "test_num_2": 1.0},
        },
        "kendall": {
            "test_num_1": {"test_num_1": 1.0, "test_num_2": 0.4285714285714286},
            "test_num_2": {"test_num_1": 0.4285714285714286, "test_num_2": 1.0},
        },
        "cramers": {
            "test_cat_1": {"test_cat_1": 1.0, "test_cat_2": 0.6614378277661477},
            "test_cat_2": {"test_cat_1": 0.6614378277661477, "test_cat_2": 1.0},
        },
        "phi_k": {
            "test_cat_2": {
                "test_cat_2": 1.0,
                "test_num_1": 1.0,
                "test_cat_1": 0.7481086232334975,
                "test_num_2": 0.7080753192907889,
            },
            "test_num_1": {
                "test_cat_2": 1.0,
                "test_num_1": 1.0,
                "test_cat_1": 1.0,
                "test_num_2": 1.0,
            },
            "test_cat_1": {
                "test_cat_2": 0.7481086232334975,
                "test_num_1": 1.0,
                "test_cat_1": 1.0,
                "test_num_2": 0.6722392716640035,
            },
            "test_num_2": {
                "test_cat_2": 0.7080753192907889,
                "test_num_1": 1.0,
                "test_cat_1": 0.6722392716640035,
                "test_num_2": 1.0,
            },
        },
    }
    return expected_results


correlations = ["pearson", "spearman", "phi_k", "cramers", "kendall"]


@pytest.mark.sparktest
@pytest.mark.parametrize("correlation_type", correlations)
def test_correlation_spark(
    correlation_data,
    correlation_type,
    expected_results,
    spark_session,
    spark_context,
):
    correlation_measures = {
        "pearson": Pearson,
        "spearman": Spearman,
        "kendall": Kendall,
        "cramers": Cramers,
        "phi_k": PhiK,
    }

    spark_df = SparkDataFrame(spark_session.createDataFrame(correlation_data["data"]))

    correlation_results = correlation_measures[correlation_type].compute(
        spark_df, correlation_data["descriptions"]
    )
    # we need to sort results by column and by index to ensure dataframes are similarly ordered
    sorted_results = correlation_results.reindex(
        sorted(correlation_results.columns), axis=1
    ).sort_index()
    sorted_expected = (
        pd.DataFrame(expected_results[correlation_type])
        .reindex(sorted(correlation_results.columns), axis=1)
        .sort_index()
    )

    # test equality, check_exact is false as correlation returns floats, 5 digits after decimal checked
    pd.testing.assert_frame_equal(sorted_results, sorted_expected, check_exact=False)


@pytest.mark.parametrize("correlation_type", correlations)
def test_not_implemented(correlation_type):
    correlation_measures = {
        "pearson": Pearson,
        "spearman": Spearman,
        "kendall": Kendall,
        "cramers": Cramers,
        "phi_k": PhiK,
    }

    with pytest.raises(NotImplementedError):
        correlation_measures[correlation_type].compute(None, None)


def test_cramers_error():
    # Key error raised when precomputed result does not contain the right keys
    with pytest.raises(KeyError):
        Cramers._cramers_corrected_stat(None, False, {"false": "error"})

    # Value error raised when input correlation matrix is not a pandas dataframe
    with pytest.raises(ValueError):
        Cramers._cramers_corrected_stat([], False, None)


def test_generic_correlations():
    with pytest.raises(NotImplementedError):
        Correlation.compute(None, None)
