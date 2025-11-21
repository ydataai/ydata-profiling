import os

import pytest

from ydata_profiling.controller import console
from ydata_profiling.utils.paths import get_config

import requests

NASA_URL = "https://data.nasa.gov/docs/legacy/meteorite_landings/Meteorite_Landings.csv"

@pytest.fixture
def console_data(get_data_file):
    try:
        return get_data_file("meteorites.csv", NASA_URL)
    except requests.RequestException as e:
        pytest.skip(f"Skipping console tests: NASA dataset unavailable ({e})")
    except Exception as e:
        pytest.skip(f"Skipping console tests: cannot fetch meteorites.csv ({e})")

@pytest.mark.skipif(os.name == "nt", reason="multiprocessing+pytest broken on Windows")
def test_console_multiprocessing(console_data, test_output_dir):
    report = test_output_dir / "test_samples.html"
    console.main(["-s", "--pool_size", "0", str(console_data), str(report)])
    assert report.exists(), "Report should exist"


def test_console_single_core(console_data, test_output_dir):
    report = test_output_dir / "test_single_core.html"
    console.main(["-s", "--pool_size", "1", str(console_data), str(report)])
    assert report.exists(), "Report should exist"


def test_console_minimal(console_data, test_output_dir):
    report = test_output_dir / "test_minimal.html"
    console.main(["-s", "--minimal", str(console_data), str(report)])
    assert report.exists(), "Report should exist"


def test_console_explorative(console_data, test_output_dir):
    report = test_output_dir / "test_explorative.html"
    console.main(
        ["-s", "--pool_size", "1", "--explorative", str(console_data), str(report)]
    )
    assert report.exists(), "Report should exist"


def test_double_config(console_data, test_output_dir):
    report = test_output_dir / "test_double_config.html"
    with pytest.raises(ValueError) as e:
        console.main(
            [
                "-s",
                "--config_file",
                str(get_config("config_default.yaml")),
                "--minimal",
                str(console_data),
                str(report),
            ]
        )

    assert (
        str(e.value) == "Arguments `config_file` and `minimal` are mutually exclusive."
    )
