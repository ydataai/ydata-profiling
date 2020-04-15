"""Main module of pandas-profiling.

.. include:: ../../README.md
"""
import json
import warnings
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from pandas_profiling.config import config
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.model.messages import MessageType
from pandas_profiling.report import get_report_structure
from pandas_profiling.utils.dataframe import rename_index
from pandas_profiling.utils.paths import get_config_default, get_config_minimal
from pandas_profiling.version import __version__


class ProfileReport(object):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.

    Used has is it will output its content as an HTML report in a Jupyter notebook.
    """

    html = ""
    """the HTML representation of the report, without the wrapper (containing `<head>` etc.)"""

    def __init__(
            self, df=None, minimal=False, config_file: Path = None, lazy=True, **kwargs
    ):
        if config_file is not None and minimal:
            raise ValueError(
                "Arguments `config_file` and `minimal` are mutually exclusive."
            )

        if df is None and not lazy:
            raise ValueError("Can init a not-lazy ProfileReport with no DataFrame")

        if minimal:
            config_file = get_config_minimal()

        if config_file:
            config.set_file(str(config_file))
        config.set_kwargs(kwargs)

        self.date_start = datetime.utcnow()
        self.date_end = None

        if lazy:  # save df, compute when needed
            # [description_set, report] will compute when needed
            self._description_set = None
            self._report = None

            if df is not None:
                # preprocess df
                self.df_hash = None  # Note that it's compute before preprocess df
                self.df = self.preprocess(df)

                # Build report structure
                self.sample = self.get_sample(df)
                self.title = config["title"].get(str)
            else:  # waiting for load
                self.df_hash = None
                self.df = None
                self.sample = {'head': None, 'tail': None}
                self.title = None
        else:  # do not save df content, compute now
            self.df = None
            # preprocess df
            df = self.preprocess(df)
            self.df_hash = joblib.hash(df)  # Note that it's compute after preprocess df

            # description_set and report will compute now
            self._description_set = describe_df(df)
            self.date_end = datetime.utcnow()

            # Build report structure
            self.sample = self.get_sample(df)
            self.title = config["title"].get(str)
            self._report = get_report_structure(
                self.date_start, self.date_end, self.sample, self.description_set
            )

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

    @property
    def description_set(self):
        if self._description_set is None:
            self._description_set = describe_df(self.df)
            self.date_end = datetime.utcnow()
        return self._description_set

    @property
    def report(self):
        if self._report is None:
            self._report = get_report_structure(
                self.date_start, self.date_end, self.sample, self.description_set
            )
        return self._report

    def get_sample(self, df: pd.DataFrame) -> dict:
        """Get head/tail samples based on the configuration

        Args:
            df: the DataFrame to sample from.

        Returns:
            A dict with the head and tail samples.
        """
        sample = {}
        n_head = config["samples"]["head"].get(int)
        if n_head > 0:
            sample["head"] = df.head(n=n_head)

        n_tail = config["samples"]["tail"].get(int)
        if n_tail > 0:
            sample["tail"] = df.tail(n=n_tail)

        return sample

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

    def to_file(self, output_file: Path, silent: bool = True) -> None:
        """Write the report to a file.

        By default a name is generated.

        Args:
            output_file: The name or the path of the file to generate including the extension (.html, .json).
            silent: if False, opens the file in the default browser
        """
        if not isinstance(output_file, Path):
            output_file = Path(str(output_file))

        if output_file.suffix == ".html":
            data = self.to_html()
        elif output_file.suffix == ".json":
            data = self.to_json()
        elif output_file.suffix == ".pp":
            self.dump(output_file)
            return
        else:
            suffix = output_file.suffix
            output_file = output_file.with_suffix(".html")
            data = self.to_html()
            warnings.warn(
                f"Extension {suffix} not supported. For now we assume .html was intended. "
                f"To remove this warning, please use .html or .json."
            )

        with output_file.open("w", encoding="utf8") as f:
            f.write(data)

        if not silent:
            import webbrowser

            webbrowser.open_new_tab(output_file.absolute().as_uri())

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string
            for using with frameworks.

        Returns:
            Profiling report html including wrapper.

        """
        from pandas_profiling.report.presentation.flavours import HTMLReport
        from pandas_profiling.report.presentation.flavours.html import templates

        use_local_assets = config["html"]["use_local_assets"].get(bool)

        html = HTMLReport(self.report).render()

        nav_items = [
            (section.name, section.anchor_id)
            for section in self.report.content["items"]
        ]
        # TODO: move to structure
        wrapped_html = templates.template("wrapper/wrapper.html").render(
            content=html,
            title=self.title,
            nav=config["html"]["navbar_show"].get(bool),
            nav_items=nav_items,
            version=__version__,
            offline=use_local_assets,
            primary_color=config["html"]["style"]["primary_color"].get(str),
            logo=config["html"]["style"]["logo"].get(str),
            theme=config["html"]["style"]["theme"].get(str),
        )

        minify_html = config["html"]["minify_html"].get(bool)
        if minify_html:
            from htmlmin.main import minify

            wrapped_html = minify(
                wrapped_html, remove_all_empty_space=True, remove_comments=True
            )
        return wrapped_html

    def to_json(self) -> str:
        class CustomEncoder(json.JSONEncoder):
            def key_to_json(self, data):
                if data is None or isinstance(data, (bool, int, str)):
                    return data
                return str(data)

            def default(self, o):
                if isinstance(o, pd.core.series.Series):
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
        from IPython.core.display import display, HTML

        report = WidgetReport(self.report).render()

        display(report)
        # TODO: move to report structure
        display(
            HTML(
                'Report generated with <a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling</a>.'
            )
        )

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

    def _repr_html_(self):
        """The ipython notebook widgets user interface gets called by the jupyter notebook."""
        self.to_notebook_iframe()

    def __repr__(self):
        """Override so that Jupyter Notebook does not print the object."""
        return ""

    def dumps(self) -> bytes:
        """
        Serialize ProfileReport and return bytes for reproducing ProfileReport or Caching.

        Returns:
            Bytes which contains hash of DataFrame, md5 of config, sample, _description_set and _report
        """
        import pickle

        if self.df_hash is None:
            self.df_hash = joblib.hash(self.df)
        return pickle.dumps(
            [
                self.df_hash,
                config.md5(),
                self.sample,
                self._description_set,
                self._report,
            ]
        )

    def loads(self, data: bytes):
        """
        Deserialize the bytes for reproducing ProfileReport or Caching.

        Args:
            data: The bytes of a serialize ProfileReport object.

        Notes:
            Load will fail if DataFrame or config unmatched

        Returns:
            self
        """
        import pickle

        try:
            df_hash, config_md5, sample, description_set, report = pickle.loads(data)
        except Exception as e:
            raise ValueError(f"Fail to load data:{e}")

        if (
                df_hash == self.df_hash or self.df_hash is None
        ) and config.md5() == config_md5:
            if self._description_set is None:
                self._description_set = description_set
            if self._report is None:
                self._report = report
            if self.sample['head'] is None or self.sample['tail'] is None:
                self.sample = sample
            self.df_hash = df_hash
            self.title = config["title"].get(str)
        else:
            raise UserWarning("DataFrame of Config is not match")
        return self

    def dump(self, output_file: Path):
        """
        Dump ProfileReport to file
        """
        if not isinstance(output_file, Path):
            output_file = Path(str(output_file))
        with output_file.open("wb") as f:
            f.write(self.dumps())

    def load(self, load_file: Path):
        """
       Load ProfileReport from file

       Notes:
            Load will fail if DataFrame or config unmatched
       """
        if not isinstance(load_file, Path):
            load_file = Path(str(load_file))
        with load_file.open("rb") as f:
            self.loads(f.read())
        return self
