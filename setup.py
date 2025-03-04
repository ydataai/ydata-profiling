from pathlib import Path

from setuptools import setup

# Read the contents of README file
source_root = Path(".")
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

try:
    version = (source_root / "VERSION").read_text().rstrip("\n")
except FileNotFoundError:
    version = "0.0.dev0"

with open(source_root / "src/ydata_profiling/version.py", "w") as version_file:
    version_file.write(f"__version__ = '{version}'")

setup(
    name="ydata-profiling",
    version=version,
    author="YData Labs Inc",
    author_email="opensource@ydata.ai",
    url="https://github.com/ydataai/ydata-profiling",
    license="MIT",
    description="Generate profile report for pandas DataFrame",
    python_requires=">=3.7, <3.13",
    install_requires=requirements,
    package_data={
        "ydata_profiling": ["py.typed"],
    },
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="pandas data-science data-analysis python jupyter ipython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    options={"bdist_wheel": {"universal": True}},
)
