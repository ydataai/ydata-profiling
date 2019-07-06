"""Configuration for the package is handled in this wrapper for confuse."""
import argparse

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
            self.config = confuse.Configuration("PandasProfiling", __name__)
            self.config.set_file(str(get_config_default()))

    def set_args(self, namespace: argparse.Namespace, dots: bool) -> None:
        """
        Set config variables based on the argparse Namespace object.

        Args:
            namespace: Dictionary or Namespace to overlay this config with. Supports nested Dictionaries and Namespaces.
            dots: If True, any properties on namespace that contain dots (.) will be broken down into child dictionaries.
        """
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
                raise ValueError('Config parameter "{}" does not exist.'.format(key))

    def set_kwargs(self, kwargs) -> None:
        """
        Helper function to set config variables based on kwargs.

        Args:
            kwargs: the arguments passed to the .profile_report() function

        """
        self._set_kwargs(self.config, kwargs)

    def __getitem__(self, item):
        return self.config[item]

    def __setitem__(self, key, value):
        self.config[key].set(value)


config = Config()
