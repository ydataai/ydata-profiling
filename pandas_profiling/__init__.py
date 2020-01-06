"""Main module of pandas-profiling.

.. include:: ../README.md
"""
import sys
import warnings
import json
from pathlib import Path

import pandas as pd
import numpy as np

from pandas_profiling.version import __version__
from pandas_profiling.utils.dataframe import clean_column_names, rename_index
from pandas_profiling.utils.paths import get_config_default, get_project_root
from pandas_profiling.config import config
from pandas_profiling.controller import pandas_decorator
from pandas_profiling.model.describe import describe as describe_df
import pandas_profiling.report.templates as templates
from pandas_profiling.report.notebook import display_notebook_iframe
from pandas_profiling.report.report import to_html


class ProfileReport(object):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.
    
    Used has is it will output its content as an HTML report in a Jupyter notebook.
    """

    html = ""
    """the HTML representation of the report, without the wrapper (containing `<head>` etc.)"""

    def __init__(self, df, config_file: Path = None, **kwargs):
        if config_file:
            config.config.set_file(str(config_file))
        config.set_kwargs(kwargs)

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

        # Render HTML
        self.minify_html = config["minify_html"].get(bool)
        self.use_local_assets = config["use_local_assets"].get(bool)
        self.title = config["title"].get(str)
        self.description_set = description_set
        self.sample = self.get_sample(df)
        self.html = to_html(self.sample, description_set)

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

    def get_sample(self, df):
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

    def get_rejected_variables(self, threshold: float = 0.9) -> list:
        """Return a list of variable names being rejected for high 
        correlation with one of remaining variables.
        
        Args:
            threshold: correlation value which is above the threshold are rejected (Default value = 0.9)

        Returns:
            A list of rejected variables.
        """
        variable_profile = self.description_set["variables"]
        result = []
        for col, values in variable_profile.items():
            if "correlation" in values:
                if values["correlation"] > threshold:
                    result.append(col)
        return result

    def to_file(self, output_file: Path, silent: bool = True) -> None:
        """Write the report to a file.
        
        By default a name is generated.

        Args:
            output_file: The name or the path of the file to generate including the extension (.html).
            silent: if False, opens the file in the default browser
        """
        if type(output_file) == str:
            output_file = Path(output_file)

        with output_file.open("w", encoding="utf8") as f:
            wrapped_html = self.to_html()
            if self.minify_html:
                from htmlmin.main import minify

                wrapped_html = minify(
                    wrapped_html, remove_all_empty_space=True, remove_comments=True
                )
            f.write(wrapped_html)

        if not silent:
            import webbrowser

            webbrowser.open_new_tab(output_file.as_uri())

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string
            for using with frameworks.

        Returns:
            Profiling report html including wrapper.
        
        """
        return templates.template("wrapper.html").render(
            content=self.html,
            title=self.title,
            correlation=len(self.description_set["correlations"]) > 0,
            missing=len(self.description_set["missing"]) > 0,
            sample=len(self.sample) > 0,
            version=__version__,
            offline=self.use_local_assets,
            primary_color=config["style"]["primary_color"].get(str),
            theme=config["style"]["theme"].get(str),
        )

    def to_json(self):
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

    def _repr_html_(self):
        """Used to output the HTML representation to a Jupyter notebook.
        When config.notebook.iframe.attribute is "src", this function creates a temporary HTML file
        in `./tmp/profile_[hash].html` and returns an Iframe pointing to that contents.
        When config.notebook.iframe.attribute is "srcdoc", the same HTML is injected in the "srcdoc" attribute of
        the Iframe.

        Notes:
            This constructions solves problems with conflicting stylesheets and navigation links.
        """
        display_notebook_iframe(self)

    def __repr__(self):
        """Override so that Jupyter Notebook does not print the object."""
        return ""
