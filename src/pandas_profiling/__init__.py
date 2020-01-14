"""Main module of pandas-profiling.

.. include:: ../../README.md
"""
import sys
import warnings
import json
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

from pandas_profiling.version import __version__
from pandas_profiling.utils.dataframe import clean_column_names, rename_index
from pandas_profiling.utils.paths import (
    get_config_default,
    get_project_root,
    get_config_minimal,
)
from pandas_profiling.config import config
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.report import get_report_structure


class ProfileReport(object):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.
    
    Used has is it will output its content as an HTML report in a Jupyter notebook.
    """

    html = ""
    """the HTML representation of the report, without the wrapper (containing `<head>` etc.)"""

    def __init__(self, df, minimal=False, config_file: Path = None, **kwargs):
        if config_file is not None and minimal:
            raise ValueError(
                "Arguments `config_file` and `minimal` are mutually exclusive."
            )

        if minimal:
            config_file = get_config_minimal()

        if config_file:
            config.config.set_file(str(config_file))
        config.set_kwargs(kwargs)

        self.date = datetime.utcnow()

        # Treat index as any other column
        if (
            not pd.Index(np.arange(0, len(df))).equals(df.index)
            or df.index.dtype != np.int64
        ):
            df = df.reset_index()

        # Rename reserved column names
        df = rename_index(df)

        # Remove spaces and colons from column names
        df = clean_column_names(df)

        # Sort names according to config (asc, desc, no sort)
        df = self.sort_column_names(df)
        config["column_order"] = df.columns.tolist()

        # Get dataset statistics
        description_set = describe_df(df)

        # Build report structure
        self.sample = self.get_sample(df)
        self.report = get_report_structure(self.date, self.sample, description_set)
        self.title = config["title"].get(str)
        self.description_set = description_set

    def sort_column_names(self, df):
        sort = config["sort"].get(str)
        if sys.version_info[1] <= 5 and sort != "None":
            warnings.warn("Sorting is supported from Python 3.6+")

        if sort in ["asc", "ascending"]:
            df = df.reindex(sorted(df.columns, key=lambda s: s.casefold()), axis=1)
        elif sort in ["desc", "descending"]:
            df = df.reindex(
                reversed(sorted(df.columns, key=lambda s: s.casefold())), axis=1
            )
        elif sort != "None":
            raise ValueError('"sort" should be "ascending", "descending" or None.')
        return df

    def get_sample(self, df: pd.DataFrame) -> dict:
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
        else:
            raise ValueError("Extension not supported (please use .html, .json)")

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

        # TODO: move to structure
        wrapped_html = templates.template("wrapper/wrapper.html").render(
            content=html,
            title=self.title,
            correlation=len(self.description_set["correlations"]) > 0,
            missing=len(self.description_set["missing"]) > 0,
            sample=len(self.sample) > 0,
            version=__version__,
            offline=use_local_assets,
            primary_color=config["html"]["style"]["primary_color"].get(str),
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
            def default(self, o):
                if isinstance(o, pd.core.series.Series) or isinstance(
                    o, pd.core.frame.DataFrame
                ):
                    return {"__{}__".format(o.__class__.__name__): o.to_json()}
                if isinstance(o, np.integer):
                    return {"__{}__".format(o.__class__.__name__): o.tolist()}

                return {"__{}__".format(o.__class__.__name__): str(o)}

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
        from pandas_profiling.report.presentation.flavours import QtReport
        from PyQt5 import QtCore
        from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout

        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QApplication([])

        class Application(QMainWindow):
            def __init__(self, widgets):
                super().__init__()
                self.layout = QVBoxLayout(self)

                self.resize(1200, 900)
                self.setWindowTitle("Pandas Profiling Report")
                self.setCentralWidget(widgets)
                self.show()

        app_widgets = QtReport(self.report).render()

        ex = Application(app_widgets)
        sys.exit(app.exec_())
