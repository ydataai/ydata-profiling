from pathlib import Path

from setuptools import setup

# Read the contents of README file
source_root = Path(".")

try:
    version = (source_root / "VERSION").read_text().rstrip("\n")
except FileNotFoundError:
    version = "0.0.dev0"

with open(source_root / "src/ydata_profiling/version.py", "w") as version_file:
    version_file.write(f"__version__ = '{version}'")

setup(
    version=version,
)
