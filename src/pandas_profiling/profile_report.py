import json
import warnings
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.model.messages import MessageType
from pandas_profiling.report import get_report_structure
from pandas_profiling.serialize import Serialize
from pandas_profiling.utils.dataframe import hash_dataframe, rename_index
from pandas_profiling.utils.paths import get_config_minimal


class ProfileReport(Serialize, object):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.

    Used has is it will output its content as an HTML report in a Jupyter notebook.
    """

    html = ""
    """the HTML representation of the report, without the wrapper (containing `<head>` etc.)"""

    def __init__(
        self,
        df=None,
        minimal=False,
        config_file: Union[Path, str] = None,
        lazy: bool = True,
        **kwargs,
    ):
        """Generate a ProfileReport based on a pandas DataFrame

        Args:
            df: the pandas DataFrame
            minimal: minimal mode is a default configuration with minimal computation
            config_file: a config file (.yml), mutually exclusive with `minimal`
            lazy: compute when needed
            **kwargs: other arguments, for valid arguments, check the default configuration file.
        """
        if config_file is not None and minimal:
            raise ValueError(
                "Arguments `config_file` and `minimal` are mutually exclusive."
            )

        if df is None and not lazy:
            raise ValueError("Can init a not-lazy ProfileReport with no DataFrame")

        if config_file:
            config.set_file(config_file)
        elif minimal:
            config.set_file(get_config_minimal())
        elif not config.is_default:
            pass
            # TODO: logging instead of warning
            # warnings.warn(
            #     "Currently configuration is not the default, if you want to restore "
            #     "default configuration, please run 'pandas_profiling.clear_config()'"
            # )

        config.set_kwargs(kwargs)

        self.df = None
        self._df_hash = -1
        self._description_set = None
        self._title = None
        self._report = None

        if df is not None:
            # preprocess df
            self.df = self.preprocess(df)

        if not lazy:
            # Trigger building the report structure
            _ = self.report

    def set_variables(self, **vars):
        config.set_kwargs(vars)

    @property
    def description_set(self):
        if self._description_set is None:
            _ = self.df_hash
            self._description_set = describe_df(self.title, self.df)
        return self._description_set

    @property
    def title(self):
        if self._title is None:
            self._title = config["title"].get(str)

        return self._title

    @property
    def df_hash(self):
        if self._df_hash == -1 and self.df is not None:
            self._df_hash = hash_dataframe(self.df)
        return self._df_hash

    @property
    def report(self):
        if self._report is None:
            self._report = get_report_structure(self.description_set)
        return self._report

    def get_duplicates(self, df=None) -> Optional[pd.DataFrame]:
        """Get duplicate rows and counts based on the configuration

        Args:
            df: Deprecated, for compatibility

        Returns:
            A DataFrame with the duplicate rows and their counts.
        """
        return self.description_set["duplicates"]

    def get_sample(self, df=None) -> dict:
        """Get head/tail samples based on the configuration

        Args:
            df: Deprecated, for compatibility

        Returns:
            A dict with the head and tail samples.
        """
        return self.description_set["sample"]

    def get_description(self) -> dict:
        """Return the description (a raw statistical summary) of the dataset.

        Returns:
            Dict containing a description for each variable in the DataFrame.
        """
        return self.description_set

    def get_rejected_variables(self) -> set:
        """Get variables that are rejected for analysis (e.g. constant, mixed data types)

        Returns:
            a set of column names that are unsupported
        """
        return {
            message.column_name
            for message in self.description_set["messages"]
            if message.message_type == MessageType.REJECTED
        }

    def to_file(self, output_file: Union[str, Path], silent: bool = True) -> None:
        """Write the report to a file.

        By default a name is generated.

        Args:
            output_file: The name or the path of the file to generate including the extension (.html, .json).
            silent: if False, opens the file in the default browser or download it in a Google Colab environment
        """
        if not isinstance(output_file, Path):
            output_file = Path(str(output_file))

        # TODO: add exporting progress bar

        binary = False
        if output_file.suffix == ".json":
            data = self.to_json()
        elif output_file.suffix == ".pp":
            data = self.dumps()
            binary = True
        else:
            data = self.to_html()
            if output_file.suffix != ".html":
                suffix = output_file.suffix
                output_file = output_file.with_suffix(".html")
                warnings.warn(
                    f"Extension {suffix} not supported. For now we assume .html was intended. "
                    f"To remove this warning, please use .html or .json."
                )

        if binary:
            output_file.write_bytes(data)
        else:
            output_file.write_text(data, encoding="utf-8")

        if not silent:
            try:
                from google.colab import files

                files.download(output_file.absolute().as_uri())
            except ModuleNotFoundError:
                import webbrowser

                webbrowser.open_new_tab(output_file.absolute().as_uri())

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string
            for using with frameworks.

        Returns:
            Profiling report html including wrapper.

        """
        from pandas_profiling.report.presentation.flavours import HTMLReport

        html = HTMLReport(self.report).render(
            nav=config["html"]["navbar_show"].get(bool),
            offline=config["html"]["use_local_assets"].get(bool),
            primary_color=config["html"]["style"]["primary_color"].get(str),
            logo=config["html"]["style"]["logo"].get(str),
            theme=config["html"]["style"]["theme"].get(str),
            title=self.description_set["analysis"]["title"],
            date=self.description_set["analysis"]["date_start"],
            version=self.description_set["package"]["pandas_profiling_version"],
        )

        minify_html = config["html"]["minify_html"].get(bool)
        if minify_html:
            from htmlmin.main import minify

            html = minify(html, remove_all_empty_space=True, remove_comments=True)
        return html

    def to_json(self) -> str:
        """Represent the ProfileReport as a JSON string

        Returns:
            JSON string
        """

        class CustomEncoder(json.JSONEncoder):
            def key_to_json(self, data):
                if data is None or isinstance(data, (bool, int, str)):
                    return data
                return str(data)

            def default(self, o):
                if isinstance(o, pd.Series):
                    return self.default(o.to_dict())

                if isinstance(o, np.integer):
                    return o.tolist()

                if isinstance(o, dict):
                    return {self.key_to_json(key): self.default(o[key]) for key in o}

                return str(o)

        return json.dumps(self.description_set, indent=4, cls=CustomEncoder)

    def to_notebook_iframe(self):
        """Used to output the HTML representation to a Jupyter notebook.
        When config.notebook.iframe.attribute is "src", this function creates a temporary HTML file
        in `./tmp/profile_[hash].html` and returns an Iframe pointing to that contents.
        When config.notebook.iframe.attribute is "srcdoc", the same HTML is injected in the "srcdoc" attribute of
        the Iframe.

        Notes:
            This constructions solves problems with conflicting stylesheets and navigation links.
        """
        from pandas_profiling.report.presentation.flavours.widget.notebook import (
            get_notebook_iframe,
        )
        from IPython.core.display import display

        display(get_notebook_iframe(self))

    def to_widgets(self):
        """The ipython notebook widgets user interface."""
        from pandas_profiling.report.presentation.flavours import WidgetReport
        from IPython.core.display import display

        report = WidgetReport(self.report).render()
        display(report)

    def _repr_html_(self):
        """The ipython notebook widgets user interface gets called by the jupyter notebook."""
        self.to_notebook_iframe()

    def __repr__(self):
        """Override so that Jupyter Notebook does not print the object."""
        return ""

    def to_app(self):
        """
        (Experimental) PyQt5 user interface, not ready to be used.
        You are welcome to contribute a pull request if you like this feature.
        """
        from pandas_profiling.report.presentation.flavours.qt.app import get_app
        from pandas_profiling.report.presentation.flavours import QtReport

        from PyQt5 import QtCore
        from PyQt5.QtWidgets import QApplication

        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QApplication([])

        app_widgets = QtReport(self.report).render()
        app = get_app(app, self.title, app_widgets)

    @staticmethod
    def preprocess(df):
        # Treat index as any other column
        if (
            not pd.Index(np.arange(0, len(df))).equals(df.index)
            or df.index.dtype != np.int64
        ):
            df = df.reset_index()

        # Rename reserved column names
        df = rename_index(df)

        # Ensure that columns are strings
        df.columns = df.columns.astype("str")
        return df

    @staticmethod
    def clear_config():
        """
        Restore the configuration to default
        """
        config.clear()
