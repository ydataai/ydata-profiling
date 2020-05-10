import numpy as np
import pandas as pd

import pandas_profiling


def test_html_export_svg():
    n_rows = 10
    n_columns = 500

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(minimal=True, html={"inline": False},)

    profile.to_file("export_svg.html")


def test_html_export_png():
    n_rows = 10
    n_columns = 500

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(minimal=True, html={"inline": False},)

    profile.to_file("export_png.html")


def test_html_export_cdn():
    n_rows = 10
    n_columns = 500

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(
        minimal=True, html={"inline": False, "use_local_assets": False},
    )

    profile.to_file("cdn.html")
    # asset no bootstrap etc.


def test_multiple_times():
    n_rows = 10
    n_columns = 500

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(minimal=True, html={"inline": False},)

    profile.to_file("cdn.html")
    profile.to_file("cdn2.html")
    profile.to_file("cdn3.html")
