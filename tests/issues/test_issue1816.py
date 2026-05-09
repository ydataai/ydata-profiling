"""
Test for issue 1816:
https://github.com/Data-Centric-AI-Community/fg-data-profiling/issues/1816

`pkg_resources` was removed in setuptools >= 81. Importing
`data_profiling.profile_report` (or its public re-exports) must not pull
`pkg_resources` in, or the import chain crashes with
``ModuleNotFoundError: No module named 'pkg_resources'`` on environments
where setuptools >= 81 has been installed (e.g. fresh CI runners).

The two regressions guards below are designed so they would fail on the
pre-fix tree even when ``setuptools`` is present (because the import
statement would still bring `pkg_resources` into ``sys.modules``), and
they exercise the actual code path (``ProfileReport.to_file``) that used
``pkg_resources.get_distribution("Pillow").version``.
"""

import importlib
import sys

import pandas as pd

from data_profiling import ProfileReport


def test_profile_report_module_does_not_import_pkg_resources():
    """The module must not pull `pkg_resources` into ``sys.modules``.

    Asserting *non-import* is the load-bearing check: setuptools 81 raises
    ``ModuleNotFoundError`` from any ``import pkg_resources``, so any
    transitive import from ``data_profiling.profile_report`` would crash
    on those environments.
    """
    sys.modules.pop("pkg_resources", None)
    sys.modules.pop("data_profiling.profile_report", None)
    importlib.import_module("data_profiling.profile_report")
    assert "pkg_resources" not in sys.modules


def test_versions_helper_does_not_import_pkg_resources():
    """`utils.versions` previously had a `pkg_resources` fallback branch.

    With Python 3.10+ (the project's floor), `importlib.metadata.version`
    is always available, so the fallback is dead code. Removing it is
    what closes the issue end-to-end.
    """
    sys.modules.pop("pkg_resources", None)
    sys.modules.pop("data_profiling.utils.versions", None)
    importlib.import_module("data_profiling.utils.versions")
    assert "pkg_resources" not in sys.modules


def test_to_file_runs_without_pkg_resources(test_output_dir):
    """End-to-end smoke: writing a report exercises the Pillow-version
    branch that previously called ``pkg_resources.get_distribution``."""
    sys.modules.pop("pkg_resources", None)
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    profile = ProfileReport(df, minimal=True)
    output_file = test_output_dir / "issue1816.html"
    profile.to_file(output_file)
    assert output_file.exists()
    # `to_file` must not have re-imported `pkg_resources` either.
    assert "pkg_resources" not in sys.modules
