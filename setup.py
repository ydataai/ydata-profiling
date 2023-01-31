import os
import sys
from pathlib import Path

from setuptools import find_packages, setup

if not ("sdist" in sys.argv or "bdist_wheel" in sys.argv):
    accept_deprecated_pandas_profiling_package_install = os.environ.get(
        "ALLOW_DEPRECATED_PANDAS_PROFILING_PACKAGE_INSTALL", ""
    ).lower()

    if accept_deprecated_pandas_profiling_package_install != "true":
        raise SystemExit(
            "*** The 'pandas-profiling' PyPI package is deprecated, please install 'ydata-profiling' instead ***"
        )

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

try:
    version = (source_root / "VERSION").read_text().rstrip("\n")
except FileNotFoundError:
    version = "0.0.dev0"

setup(
    name="pandas-profiling",
    version=version,
    author="YData Labs Inc",
    author_email="opensource@ydata.ai",
    url="https://github.com/ydataai/pandas-profiling",
    license="MIT",
    description="Deprecated 'pandas-profiling' package, use 'ydata-profiling' instead",
    python_requires=">=3.7, <3.11",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
    ],
    keywords="pandas data-science data-analysis python jupyter ipython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    options={"bdist_wheel": {"universal": True}},
)
