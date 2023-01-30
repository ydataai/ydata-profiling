import pytest

from ydata_profiling.utils.dataframe import sort_column_names


@pytest.fixture()
def input_variables():
    return {"var1": None, "Boolean": None, "Python": None, "#0": None}


@pytest.mark.parametrize("sort", [None])
def test_none(sort, input_variables):
    expected_variables = {"var1": None, "Boolean": None, "Python": None, "#0": None}
    sorted_variables = sort_column_names(input_variables, sort)
    assert tuple(sorted_variables.keys()) == tuple(expected_variables.keys())


@pytest.mark.parametrize("sort", ["asc", "ascending", "ASC"])
def test_ascending(sort, input_variables):
    expected_variables = {"#0": None, "Boolean": None, "Python": None, "var1": None}
    sorted_variables = sort_column_names(input_variables, sort)
    assert tuple(sorted_variables.keys()) == tuple(expected_variables.keys())


@pytest.mark.parametrize("sort", ["desc", "descending", "DESC"])
def test_descending(sort, input_variables):
    expected_variables = {"var1": None, "Python": None, "Boolean": None, "#0": None}
    sorted_variables = sort_column_names(input_variables, sort)
    assert tuple(sorted_variables.keys()) == tuple(expected_variables.keys())
