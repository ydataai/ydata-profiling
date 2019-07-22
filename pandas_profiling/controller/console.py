"""This file add the console interface to the package."""
from pathlib import Path

import pandas as pd
import pandas_profiling
from pandas_profiling import __version__
from pandas_profiling.config import config
import argparse

from pandas_profiling.utils.dataframe import read_pandas


def parse_args(args: list or None = None) -> argparse.Namespace:
    """Parse the command line arguments for the `pandas_profiling` binary.

    Args:
      args: List of input arguments. (Default value=None).

    Returns:
      Namespace with parsed arguments.

    """
    parser = argparse.ArgumentParser(
        description="Profile the variables in a CSV file and generate a HTML report."
    )

    # Version
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
    )

    # Console specific
    parser.add_argument(
        "-s",
        "--silent",
        help="Only generate but do not open report",
        action="store_true",
    )

    # Config
    parser.add_argument(
        "--pool_size", type=int, default=0, help="Number of CPU cores to use"
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Pandas Profiling Report",
        help="Title for the report",
    )
    parser.add_argument(
        "input_file",
        type=Path,
        help="CSV file (or other file type supported by pandas) to profile",
    )
    parser.add_argument("output_file", type=Path, help="Output report file")

    return parser.parse_args(args)


def main(args=None) -> None:
    """ Run the `pandas_profiling` package.

    Args:
      args: Arguments for the programme (Default value=None).
    """

    # Parse the arguments
    args = parse_args(args)
    config.set_args(args, dots=True)

    # read the DataFrame
    df = read_pandas(args.input_file)

    # Generate the profiling report
    p = df.profile_report()
    p.to_file(output_file=args.output_file)

    # Open a webbrowser tab if requested
    if not args.silent:
        import webbrowser

        webbrowser.open_new_tab(args.output_file)
