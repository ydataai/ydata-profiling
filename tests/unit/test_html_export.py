from pathlib import Path

import numpy as np
import pandas as pd

import pandas_profiling


def check_assets(assets_dir: Path, file_type, n_css, n_js):
    """Check that files and dirs exist

    Args:
        assets_dir: directory of the assets
        file_type: png/svg
    """
    assert assets_dir.is_dir()
    images_dir = assets_dir / "images"
    assert images_dir.is_dir()
    css_dir = assets_dir / "css"
    assert css_dir.is_dir()
    js_dir = assets_dir / "js"
    assert js_dir.is_dir()

    assert all(file.suffix == f".{file_type}" for file in images_dir.glob("*"))
    assert all(file.suffix == ".css" for file in css_dir.glob("*"))
    assert all(file.suffix == ".js" for file in js_dir.glob("*"))
    assert (len(list(js_dir.glob("*")))) == n_js
    assert (len(list(css_dir.glob("*")))) == n_css


def test_html_export_svg(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(minimal=True, html={"inline": False})

    report = test_output_dir / "export_svg.html"
    profile.to_file(report)
    assert report.exists()
    assets_dir = test_output_dir / "export_svg_assets"
    check_assets(assets_dir, "svg", n_css=3, n_js=3)


def test_html_export_png(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(
        minimal=True, html={"inline": False}, plot={"image_format": "png"}
    )

    report = test_output_dir / "export_png.html"
    profile.to_file(report)
    assert report.exists()
    assets_dir = test_output_dir / "export_png_assets"
    check_assets(assets_dir, "png", n_css=3, n_js=3)


def test_html_export_cdn(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(
        minimal=True, html={"inline": False, "use_local_assets": False},
    )

    report = test_output_dir / "cdn.html"
    profile.to_file(report)
    assert report.exists()
    assets_dir = test_output_dir / "cdn_assets"
    check_assets(assets_dir, "svg", n_css=1, n_js=1)


def test_html_export_theme(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(
        minimal=True, html={"inline": False, "style": {"theme": "united"}},
    )

    report = test_output_dir / "united.html"
    profile.to_file(report)
    assert report.exists()
    assets_dir = test_output_dir / "united_assets"
    check_assets(assets_dir, "svg", n_css=2, n_js=3)


def test_multiple_times(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(
        minimal=True, html={"inline": False, "use_local_assets": False}
    )

    report = test_output_dir / "cdn_multi.html"
    profile.to_file(report)
    n_images = len(list(Path("./cdn_multi_assets/").joinpath("images").glob("*")))
    assert report.exists()
    assets_dir = test_output_dir / "cdn_multi_assets"
    check_assets(assets_dir, "svg", n_css=1, n_js=1)
    profile.to_file(report)
    assert report.exists()
    assert n_images == len(
        list(Path("./cdn_multi_assets/").joinpath("images").glob("*"))
    )


def test_subdir(test_output_dir):
    n_rows = 10
    n_columns = 10

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )

    profile = df.profile_report(minimal=True, html={"inline": False})

    subdir_path = test_output_dir / "subdir"
    subdir_path.mkdir()
    subdir_path.joinpath("test.py").touch()
    report = subdir_path / "subdir.html"
    profile.to_file(report)
    assert report.exists()
    assets_dir = subdir_path / "subdir_assets"
    check_assets(assets_dir, "svg", n_css=3, n_js=3)
    assert subdir_path.joinpath("test.py").exists()
