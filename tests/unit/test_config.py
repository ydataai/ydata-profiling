from ydata_profiling import ProfileReport


def test_set_variable():
    r = ProfileReport(pool_size=3)
    assert r.config.pool_size == 3
    assert r.config.html.minify_html
    r.config.pool_size = 1
    assert r.config.pool_size == 1
    r.config.html.minify_html = False
    assert not r.config.html.minify_html
    r.config.html.minify_html = True
    assert r.config.html.minify_html


def test_config_shorthands():
    r = ProfileReport(
        samples=None, correlations=None, missing_diagrams=None, duplicates=None
    )
    assert r.config.samples.head == 0
    assert r.config.samples.tail == 0
    assert r.config.duplicates.head == 0
    assert not r.config.correlations["spearman"].calculate
    assert not r.config.missing_diagrams["bar"]


def test_config_env(monkeypatch):
    monkeypatch.setenv("PROFILE_TITLE", "Testing Title")
    monkeypatch.setenv("PROFILE_PLOT", '{"dpi": 1000}')

    r = ProfileReport()
    assert r.config.title == "Testing Title"
    assert r.config.plot.dpi == 1000
