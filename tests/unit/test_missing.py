import pandas as pd
import pytest
from pandas_profiling.model.data import ConfMatrixData

test_data = [
    (
        pd.DataFrame([[77, 404], [16, 122]]),
        pd.DataFrame([[0.16, 0.84], [0.116, 0.884]]),
        0.201,
    ),
]


@pytest.mark.parametrize("absolute_data, relative_data, expected_p_value", test_data)
def test_missing_conf_matrix(absolute_data, relative_data, expected_p_value):
    missing_conf = ConfMatrixData(absolute_data, relative_data)
    assert round(missing_conf.p_value, 3) == expected_p_value
