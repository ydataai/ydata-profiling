import matplotlib
import pandas as pd
import pytest
from matplotlib import pyplot as plt

from pandas_profiling.visualisation.plot import _plot_pie_chart, _plot_stacked_barh

# Generating dummy data
ids = ["bool", "cat"]
dummy_bool_data = pd.Series({True: 82, False: 36})
dummy_cat_data = pd.Series(
    {
        "Amadeou_plus": 75,
        "Beta_front": 50,
        "Calciumus": 20,
        "Dimitrius": 1,
        "esperagus_anonymoliumus": 75,
        "FrigaTTTBrigde_Writap": 50,
        "galgarartiy": 30,
        "He": 1,
        "I": 10,
        "JimISGODDOT": 1,
    }
)

default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]  # careful max is 10


# Unit tests
@pytest.mark.parametrize("data", [dummy_bool_data, dummy_cat_data], ids=ids)
def test_plot_stacked_barh(data):
    ax, legend = _plot_stacked_barh(
        data=data,
        colors=default_colors[: len(data)],
    )
    assert issubclass(type(ax), plt.Axes)  # test that a matplotlib plot is retrned
    assert issubclass(type(legend), matplotlib.legend.Legend)


@pytest.mark.parametrize("data", [dummy_bool_data, dummy_cat_data], ids=ids)
def test_plot_pie_chart(data):
    ax, legend = _plot_pie_chart(
        data=data,
        colors=default_colors[: len(data)],
    )
    assert issubclass(type(ax), plt.Axes)  # test that a matplotlib plot is retrned
    assert issubclass(type(legend), matplotlib.legend.Legend)
