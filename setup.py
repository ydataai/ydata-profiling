from pathlib import Path

from setuptools import find_packages, setup

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

try:
    version = (source_root / "VERSION").read_text().rstrip("\n")
except FileNotFoundError:
    version = "0.0.dev0"

with open(source_root / "src/pandas_profiling/version.py", "w") as version_file:
    version_file.write(f"__version__ = '{version}'")

setup(
    name="pandas-profiling",
    version=version,
    author="YData Labs Inc",
    author_email="opensource@ydata.ai",
    packages=find_packages("src"),
    package_dir={"": "src"},
    url="https://github.com/ydataai/pandas-profiling",
    license="MIT",
    description="Deprecated 'pandas-profiling' package, use 'ydata-profiling' instead",
    python_requires=">=3.7, <3.11",
    install_requires=[
        "ydata-profiling",
    ],
    extras_require={
        "notebook": [
            "jupyter-client>=5.3.4",
            "jupyter-core>=4.6.3",
            "ipywidgets>=7.5.1",
        ],
        "unicode": [
            "tangled-up-in-unicode==0.2.0",
        ],
    },
    package_data={
        "pandas_profiling": ["py.typed"],
    },
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
    entry_points={
        "console_scripts": [
            "pandas_profiling = pandas_profiling.controller.console:main"
        ]
    },
    options={"bdist_wheel": {"universal": True}},
)
