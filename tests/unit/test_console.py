from pandas_profiling.controller import console


def test_console_multiprocessing(tmpdir):
    report = tmpdir / "test_samples.html"
    console.main(
        [
            "-s",
            "--pool_size",
            "0",
            "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
            str(report),
        ]
    )
    assert report.exists(), "Report should exist"


def test_console_single_core(tmpdir):
    report = tmpdir / "test_single_core.html"
    console.main(
        [
            "-s",
            "--pool_size",
            "1",
            "https://data.nasa.gov/api/views/gh4g-9sfh/rows.csv?accessType=DOWNLOAD",
            str(report),
        ]
    )
    assert report.exists(), "Report should exist"
