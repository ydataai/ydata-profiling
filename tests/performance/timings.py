import math
import timeit
from itertools import product
from string import ascii_lowercase

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from pandas_profiling import ProfileReport


def make_sample_data(cols, rows):
    iters = math.ceil(cols / 26)
    column_names = []
    for x in range(1, iters + 1):
        column_names += list(product(ascii_lowercase, repeat=x))

    column_names = [x[0] for x in column_names]

    df = pd.DataFrame(
        np.random.randint(0, 1000000, size=(rows, cols)), columns=column_names[0:cols]
    )

    assert df.shape == (rows, cols)
    return df


def make_report_minimal(df):
    report = ProfileReport(
        df,
        minimal=True,
        pool_size=0,
        title="Dataset with <em>Numeric</em> Categories",
    )
    html = report.to_html()
    assert type(html) == str and '<p class="h2">Dataset info</p>' in html


def make_report(df):
    report = ProfileReport(
        df,
        minimal=False,
        pool_size=0,
        title="Dataset with <em>Numeric</em> Categories",
    )
    html = report.to_html()
    assert type(html) == str and '<p class="h2">Dataset info</p>' in html


def wrap_func(function):
    def inner(df):
        def double_inner():
            return function(df)

        return double_inner

    return inner


def time_report(func, cols, rows, runs=5):
    df = make_sample_data(cols, rows)
    print(df.shape, cols, rows)
    print(df.head())
    test = wrap_func(func)(df)
    return timeit.timeit(test, number=runs) / runs


def plot_col_run_time():
    cols = [1, 2, 4, 10, 50]
    row = 1000
    default_times = [time_report(make_report, col, row) for col in cols]
    minimal_times = [time_report(make_report_minimal, col, row) for col in cols]

    ax1 = sns.scatterplot(cols, default_times)
    ax = sns.scatterplot(cols, minimal_times)
    _ = ax1.set(
        xlabel=f"Number of columns (row={row})",
        ylabel="time (s)",
        title="Run Time Complexity",
    )
    plt.show()


def plot_row_run_time():
    # 10, 100
    # https://github.com/pandas-profiling/pandas-profiling/issues/270
    rows = [1000, 10000, 100000]
    col = 10
    default_times = [time_report(make_report, col, row) for row in rows]
    minimal_times = [time_report(make_report_minimal, col, row) for row in rows]

    ax1 = sns.scatterplot(rows, default_times)
    ax2 = sns.scatterplot(rows, minimal_times)
    _ = ax1.set(
        xlabel=f"Number of rows (col={col})",
        ylabel="time (s)",
        title="Run Time Complexity",
    )
    plt.show()


if __name__ == "__main__":
    # plot_col_run_time()
    plot_row_run_time()
