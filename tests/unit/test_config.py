from multiprocessing import Pool

import pandas as pd

from pandas_profiling import ProfileReport


def profile_report(kwargs):
    profile = ProfileReport(**kwargs)
    return profile.description_set["analysis"]["title"], profile.to_json()


def test_config_mutiprocess():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 1, 1, 1], "b": [1, 2, 3, 4, 5, 6], "c": [1, 2, 3, 4, 5, 6]}
    )
    pool = Pool(processes=2)

    ret0 = pool.apply_async(
        profile_report, args=({"df": df, "minimal": True, "title": "minimal-report"},)
    )
    ret1 = pool.apply_async(
        profile_report, args=({"df": df, "minimal": False, "title": "default-report"},)
    )

    pool.close()
    pool.join()

    profile0_title, profile0_json = ret0.get()
    profile1_title, profile1_json = ret1.get()

    assert profile0_json != profile1_json
    assert profile0_title == "minimal-report"
    assert profile1_title == "default-report"


def test_set_variable():
    r = ProfileReport(pool_size=3)
    assert r.config["pool_size"].get(int) == 3
    assert r.config["html"]["minify_html"].get(bool)
    r.set_variable("pool_size", 1)
    assert r.config["pool_size"].get(int) == 1
    r.set_variable("html.minify_html", False)
    assert not r.config["html"]["minify_html"].get(bool)
    r.set_variable("html", {"minify_html": True})
    assert r.config["html"]["minify_html"].get(bool)


def test_config_shorthands():
    r = ProfileReport(
        samples=None, correlations=None, missing_diagrams=None, duplicates=None
    )
    assert r.config["samples"]["head"].get(int) == 0
    assert r.config["samples"]["tail"].get(int) == 0
    assert r.config["duplicates"]["head"].get(int) == 0
    assert not r.config["correlations"]["spearman"]["calculate"].get(bool)
    assert not r.config["missing_diagrams"]["bar"].get(bool)

    r = ProfileReport()
    r.set_variable("samples", None)
    r.set_variable("duplicates", None)
    r.set_variable("correlations", None)
    r.set_variable("missing_diagrams", None)

    assert r.config["samples"]["head"].get(int) == 0
    assert r.config["samples"]["tail"].get(int) == 0
    assert r.config["duplicates"]["head"].get(int) == 0
    assert not r.config["correlations"]["spearman"]["calculate"].get(bool)
    assert not r.config["missing_diagrams"]["bar"].get(bool)
