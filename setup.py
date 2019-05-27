from pandas_profiling.utils.paths import get_project_root
from setuptools import setup, find_packages

# Read the contents of README file
source_root = get_project_root()
with (source_root / "README.md").open(encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pandas-profiling",
    version="2.0.0",
    author="Jos Polfliet, Simon Brugman",
    author_email="simon@graphkite.nl",
    packages=find_packages(),
    url="https://github.com/pandas-profiling/pandas-profiling",
    license="MIT",
    description="Generate profile report for pandas DataFrame",
    install_requires=[
        "pandas>=0.19",
        "matplotlib>=1.4",
        "jinja2>=2.8",
        "missingno",
        "htmlmin",
        "phik",
        "confuse",
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "Framework :: IPython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="pandas data-science data-analysis python jupyter ipython",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "pandas_profiling = pandas_profiling.entry.profile_csv:main"
        ]
    },
)
