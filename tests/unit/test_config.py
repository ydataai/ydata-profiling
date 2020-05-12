from pandas_profiling import ProfileReport
from pandas_profiling.config import config


def test_set_variable():
    r = ProfileReport(pool_size=3)
    assert config["pool_size"].get(int) == 3
    assert config["html"]["minify_html"].get(bool)
    r.set_variable("pool_size", 1)
    assert config["pool_size"].get(int) == 1
    r.set_variable("html.minify_html", False)
    assert not config["html"]["minify_html"].get(bool)
    r.set_variable("html", {"minify_html": True})
    assert config["html"]["minify_html"].get(bool)


def test_config_shorthands():
    r = ProfileReport(
        samples=None, correlations=None, missing_diagrams=None, duplicates=None
    )
    assert config["samples"]["head"].get(int) == 0
    assert config["samples"]["tail"].get(int) == 0
    assert config["duplicates"]["head"].get(int) == 0
    assert not config["correlations"]["spearman"]["calculate"].get(bool)
    assert not config["missing_diagrams"]["bar"].get(bool)

    r = ProfileReport()
    r.set_variable("samples", None)
    r.set_variable("duplicates", None)
    r.set_variable("correlations", None)
    r.set_variable("missing_diagrams", None)

    assert config["samples"]["head"].get(int) == 0
    assert config["samples"]["tail"].get(int) == 0
    assert config["duplicates"]["head"].get(int) == 0
    assert not config["correlations"]["spearman"]["calculate"].get(bool)
    assert not config["missing_diagrams"]["bar"].get(bool)
