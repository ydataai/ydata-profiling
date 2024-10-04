import pandas as pd

from ydata_profiling.utils.cache import cache_file


def test_dataset_schema():
    file_name = cache_file("auto2.dta", "http://www.stata-press.com/data/r15/auto2.dta")
    df = pd.read_stata(file_name)

    metadata = {
        "creator": "Firstname Lastname",
        "author": "Firstname Lastname",
        "description": "This profiling report was generated using a sample of 5% of the original dataset.",
        "copyright_holder": "RandoCorp LLC",
        "copyright_year": "2020",
        "url": "http://www.dataset-sources.com/data/dataset.dat",
    }

    # Length left out due to correlation with weight.
    report = df.profile_report(
        title="Dataset schema",
        dataset=metadata,
        minimal=True,
    )

    html = report.to_html()

    assert ">Dataset<" in html
    for key in metadata.keys():
        if not key.startswith("copyright_") and key != "url":
            assert f"<th>{key.capitalize()}</th>" in html
    assert "<tr><th>Copyright</th><td>(c) RandoCorp LLC 2020</td></tr>"
    assert '<tr><th>URL</th><td><a href="http://www.dataset-sources.com/data/dataset.dat">http://www.dataset-sources.com/data/dataset.dat</a></td></tr>'
    assert ">Reproduction<" in html


def test_dataset_schema_empty():
    file_name = cache_file("auto2.dta", "http://www.stata-press.com/data/r15/auto2.dta")
    df = pd.read_stata(file_name)

    # Length left out due to correlation with weight.
    report = df.profile_report(
        title="Dataset schema empty",
        minimal=True,
        dataset=None,
    )

    html = report.to_html()

    assert ">Dataset<" not in html
    assert ">Reproduction<" in html
