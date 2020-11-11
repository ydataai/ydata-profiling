"""Configuration for the package is handled in this wrapper for confuse."""
import argparse
from pathlib import Path
from typing import Union

import confuse

from pandas_profiling.utils.paths import get_config_default


class Config(object):
    """This is a wrapper for the python confuse package, which handles setting and getting configuration variables via
    various ways (notably via argparse and kwargs).
    """

    config = None
    """The confuse.Configuration object."""

    def __init__(self):
        """The config constructor should be called only once."""
        if self.config is None:
            self.clear()
        else:
            self.set_file(str(get_config_default()))

    def set_file(self, file_name: Union[str, Path]) -> None:
        """
        Set the config from a file

        Args:
            file_name: file name
        """
        if self.config is not None:
            self.config.set_file(str(file_name))

    _arg_groups = {
        "sensitive": {
            "samples": None,
            "duplicates": None,
            "vars": {"cat": {"redact": True}},
        },
        "dark_mode": {
            "html": {
                "style": {
                    "theme": "flatly",
                    "primary_color": "#2c3e50",
                }
            }
        },
        "orange_mode": {
            "html": {
                "style": {
                    "theme": "united",
                    "primary_color": "#d34615",
                }
            }
        },
        "explorative": {
            "vars": {
                "cat": {"unicode": True},
                "file": {"active": True},
                "image": {
                    "active": True,
                },
            },
            "n_obs_unique": 10,
            "n_extreme_obs": 10,
            "n_freq_table_max": 25,
            "memory_deep": True,
        },
    }

    def set_arg_group(self, name):
        for key, value in self._arg_groups[name].items():
            self.set_kwargs({key: value})

    def set_args(self, namespace: argparse.Namespace, dots: bool) -> None:
        """
        Set config variables based on the argparse Namespace object.

        Args:
            namespace: Dictionary or Namespace to overlay this config with. Supports nested Dictionaries and Namespaces.
            dots: If True, any properties on namespace that contain dots (.) will be broken down into child dictionaries.
        """
        if self.config is not None:
            self.config.set_args(namespace, dots)

    def _set_kwargs(self, reference, values: dict):
        """Helper function to set config variables based on kwargs."""
        for key, value in values.items():
            if key in reference:
                if type(value) == dict:
                    self._set_kwargs(reference[key], value)
                else:
                    reference[key].set(value)
            else:
                raise ValueError(f'Config parameter "{key}" does not exist.')

    _shorthands = {
        "dataset": dict(
            creator="",
            author="",
            description="",
            copyright_holder="",
            copyright_year="",
            url="",
        ),
        "samples": {"head": 0, "tail": 0},
        "duplicates": {"head": 0},
        "interactions": {"targets": [], "continuous": False},
        "missing_diagrams": {
            "bar": False,
            "bar2": False,
            "matrix": False,
            "heatmap": False,
            "dendrogram": False,
        },
        "correlations": {
            "pearson": {"calculate": False},
            "spearman": {"calculate": False},
            "kendall": {"calculate": False},
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False},
        },
    }

    def _handle_shorthands(self, kwargs):
        for key, value in self._shorthands.items():
            if key in kwargs and kwargs[key] is None:
                kwargs[key] = value
        return kwargs

    def _handle_shorthand(self, key, value):
        if key in self._shorthands and value is None:
            return self._shorthands[key]
        else:
            return value

    def set_kwargs(self, kwargs) -> None:
        """
        Helper function to set config variables based on kwargs.

        Args:
            kwargs: the arguments passed to the .profile_report() function

        """
        kwargs = self._handle_shorthands(kwargs)

        self._set_kwargs(self.config, kwargs)

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        value = self._handle_shorthand(key, value)
        self.config[key].set(value)

    def dump(self):
        return self.config.dump()

    def update(self, other):
        if not isinstance(other, Config):
            raise ValueError("Can only update config from a config object")
        self.config = other.config

    def clear(self):
        self.config = confuse.Configuration("PandasProfiling", __name__, read=False)
        self.set_file(str(get_config_default()))

    @property
    def is_default(self):
        default_config = Config()
        return self == default_config

    def __eq__(self, other):
        return isinstance(other, Config) and self.dump() == other.dump()


config = Config()
