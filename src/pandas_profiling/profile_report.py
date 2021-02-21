import json
import warnings
from pathlib import Path
from typing import Any, Optional, Union

import attr
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from visions import VisionsTypeset

from pandas_profiling.config import config
from pandas_profiling.expectations_report import ExpectationsReport
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.model.messages import MessageType
from pandas_profiling.model.sample import Sample
from pandas_profiling.model.summarizer import (
    BaseSummarizer,
    PandasProfilingSummarizer,
    format_summary,
)
from pandas_profiling.model.typeset import ProfilingTypeSet
from pandas_profiling.report import get_report_structure
from pandas_profiling.report.presentation.flavours.html.templates import (
    create_html_assets,
)
from pandas_profiling.serialize_report import SerializeReport
from pandas_profiling.utils.dataframe import hash_dataframe, rename_index
from pandas_profiling.utils.paths import get_config


class ProfileReport(SerializeReport, ExpectationsReport):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.

    Used as is, it will output its content as an HTML report in a Jupyter notebook.
    """

    def __init__(
        self,
        df: Optional[pd.DataFrame] = None,
        minimal: bool = False,
        explorative: bool = False,
        sensitive: bool = False,
        dark_mode: bool = False,
        orange_mode: bool = False,
        sample: Optional[dict] = None,
        config_file: Union[Path, str] = None,
        lazy: bool = True,
        typeset: Optional[VisionsTypeset] = None,
        summarizer: Optional[BaseSummarizer] = None,
        **kwargs,
    ):
        """Generate a ProfileReport based on a pandas DataFrame

        Args:
            df: the pandas DataFrame
            minimal: minimal mode is a default configuration with minimal computation
            config_file: a config file (.yml), mutually exclusive with `minimal`
            lazy: compute when needed
            sample: optional dict(name="Sample title", caption="Caption", data=pd.DataFrame())
            typeset: optional user typeset to use for type inference
            summarizer: optional user summarizer to generate custom summary output
            **kwargs: other arguments, for valid arguments, check the default configuration file.
        """
        config.clear()  # to reset (previous) config.
        if config_file is not None and minimal:
            raise ValueError(
                "Arguments `config_file` and `minimal` are mutually exclusive."
            )

        if df is None and not lazy:
            raise ValueError("Can init a not-lazy ProfileReport with no DataFrame")

        if config_file:
            config.set_file(config_file)
        elif minimal:
            config.set_file(get_config("config_minimal.yaml"))
        elif not config.is_default:
            pass
            # warnings.warn(
            #     "Currently configuration is not the default, if you want to restore "
            #     "default configuration, please run 'pandas_profiling.clear_config()'"
            # )
        if explorative:
            config.set_arg_group("explorative")
        if sensitive:
            config.set_arg_group("sensitive")
        if dark_mode:
            config.set_arg_group("dark_mode")
        if orange_mode:
            config.set_arg_group("orange_mode")

        config.set_kwargs(kwargs)

        self.df = None
        self._df_hash = -1
        self._description_set = None
        self._sample = sample
        self._title = None
        self._report = None
        self._html = None
        self._widgets = None
        self._json = None
        self._typeset = typeset
        self._summarizer = summarizer

        if df is not None:
            # preprocess df
            self.df = self.preprocess(df)

        if not lazy:
            # Trigger building the report structure
            _ = self.report

    def set_variable(self, key: str, value: Any):
        """Change a single configuration variable

        Args:
            key: configuration parameter name. Accepts nested syntax, e.g. "html.minify_html"
            value: the new value

        Examples:
            >>> ProfileReport(df).set_variables("title", "NewTitle")
            >>> ProfileReport(df).set_variables("html", {"minify_html": False})
            >>> ProfileReport(df).set_variables("html.minify_html", False)

        """
        keys = key.split(".")
        for e in reversed(keys[1:]):
            value = {e: value}

        self.set_variables(**{keys[0]: value})

    def set_variables(self, **vars):
        """Change configuration variables (invalidates caches where necessary)

        Args:
            **vars: configuration parameters to change

        Examples:
            >>> ProfileReport(df).set_variables(title="NewTitle", html={"minify_html": False})
        """
        changed = set(vars.keys())
        if len({"progress_bar", "pool_size"} & changed) > 0:
            # Cache can persist
            pass

        if len({"notebook"} & changed) > 0:
            self._widgets = None

        if len({"html", "title"} & changed) > 0:
            self._html = None

        if not {"progress_bar", "pool_size", "notebook", "html", "title"} >= changed:
            # In all other cases, empty cache
            self._description_set = None
            self._title = None
            self._report = None
            self._html = None
            self._widgets = None
            self._json = None

        if len(vars) == 1:
            config[list(vars.keys())[0]] = list(vars.values())[0]
        else:
            config.set_kwargs(vars)

    @property
    def typeset(self):
        if self._typeset is None:
            self._typeset = ProfilingTypeSet()
        return self._typeset

    @property
    def summarizer(self):
        if self._summarizer is None:
            self._summarizer = PandasProfilingSummarizer(self.typeset)
        return self._summarizer

    @property
    def description_set(self):
        if self._description_set is None:
            self._description_set = describe_df(
                self.title, self.df, self.summarizer, self.typeset, self._sample
            )
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

    @property
    def html(self):
        if self._html is None:
            self._html = self._render_html()
        return self._html

    @property
    def json(self):
        if self._json is None:
            self._json = self._render_json()
        return self._json

    @property
    def widgets(self):
        if self._widgets is None:
            self._widgets = self._render_widgets()
        return self._widgets

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

        if output_file.suffix == ".json":
            data = self.to_json()
        else:
            inline = config["html"]["inline"].get(bool)
            if not inline:
                config["html"]["file_name"] = str(output_file)
                create_html_assets(output_file)

            data = self.to_html()

            if output_file.suffix != ".html":
                suffix = output_file.suffix
                output_file = output_file.with_suffix(".html")
                warnings.warn(
                    f"Extension {suffix} not supported. For now we assume .html was intended. "
                    f"To remove this warning, please use .html or .json."
                )

        disable_progress_bar = not config["progress_bar"].get(bool)
        with tqdm(
            total=1, desc="Export report to file", disable=disable_progress_bar
        ) as pbar:
            output_file.write_text(data, encoding="utf-8")
            pbar.update()

        if not silent:
            try:
                from google.colab import files

                files.download(output_file.absolute().as_uri())
            except ModuleNotFoundError:
                import webbrowser

                webbrowser.open_new_tab(output_file.absolute().as_uri())

    def _render_html(self):
        from pandas_profiling.report.presentation.flavours import HTMLReport

        report = self.report

        disable_progress_bar = not config["progress_bar"].get(bool)
        with tqdm(total=1, desc="Render HTML", disable=disable_progress_bar) as pbar:
            html = HTMLReport(report).render(
                nav=config["html"]["navbar_show"].get(bool),
                offline=config["html"]["use_local_assets"].get(bool),
                inline=config["html"]["inline"].get(bool),
                file_name=Path(config["html"]["file_name"].get(str)).stem,
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
            pbar.update()
        return html

    def _render_widgets(self):
        from pandas_profiling.report.presentation.flavours import WidgetReport

        report = self.report

        disable_progress_bar = not config["progress_bar"].get(bool)
        with tqdm(
            total=1, desc="Render widgets", disable=disable_progress_bar, leave=False
        ) as pbar:
            widgets = WidgetReport(report).render()
            pbar.update()
        return widgets

    def _render_json(self):
        def encode_it(o):
            if isinstance(o, dict):
                return {encode_it(k): encode_it(v) for k, v in o.items()}
            else:
                if isinstance(o, (bool, int, float, str)):
                    return o
                elif isinstance(o, list):
                    return [encode_it(v) for v in o]
                elif isinstance(o, set):
                    return {encode_it(v) for v in o}
                elif isinstance(o, (pd.DataFrame, pd.Series)):
                    return encode_it(o.to_dict(orient="records"))
                elif isinstance(o, np.ndarray):
                    return encode_it(o.tolist())
                elif isinstance(o, Sample):
                    return encode_it(attr.asdict(o))
                elif isinstance(o, np.generic):
                    return o.item()
                else:
                    return str(o)

        description = self.description_set

        disable_progress_bar = not config["progress_bar"].get(bool)
        with tqdm(total=1, desc="Render JSON", disable=disable_progress_bar) as pbar:
            description = format_summary(description)
            description = encode_it(description)
            data = json.dumps(description, indent=4)
            pbar.update()
        return data

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string
            for using with frameworks.

        Returns:
            Profiling report html including wrapper.

        """
        return self.html

    def to_json(self) -> str:
        """Represent the ProfileReport as a JSON string

        Returns:
            JSON string
        """

        return self.json

    def to_notebook_iframe(self):
        """Used to output the HTML representation to a Jupyter notebook.
        When config.notebook.iframe.attribute is "src", this function creates a temporary HTML file
        in `./tmp/profile_[hash].html` and returns an Iframe pointing to that contents.
        When config.notebook.iframe.attribute is "srcdoc", the same HTML is injected in the "srcdoc" attribute of
        the Iframe.

        Notes:
            This constructions solves problems with conflicting stylesheets and navigation links.
        """
        from IPython.core.display import display

        from pandas_profiling.report.presentation.flavours.widget.notebook import (
            get_notebook_iframe,
        )

        # Ignore warning: https://github.com/ipython/ipython/pull/11350/files
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            display(get_notebook_iframe(self))

    def to_widgets(self):
        """The ipython notebook widgets user interface."""
        try:
            from google.colab import files

            warnings.warn(
                "Ipywidgets is not yet fully supported on Google Colab (https://github.com/googlecolab/colabtools/issues/60)."
                "As an alternative, you can use the HTML report. See the documentation for more information."
            )
        except ModuleNotFoundError:
            pass

        from IPython.core.display import display

        display(self.widgets)

    def _repr_html_(self):
        """The ipython notebook widgets user interface gets called by the jupyter notebook."""
        self.to_notebook_iframe()

    def __repr__(self):
        """Override so that Jupyter Notebook does not print the object."""
        return ""

    @staticmethod
    def preprocess(df):
        """Preprocess the dataframe

        - Appends the index to the dataframe when it contains information
        - Rename the "index" column to "df_index", if exists
        - Convert the DataFrame's columns to str

        Args:
            df: the pandas DataFrame

        Returns:
            The preprocessed DataFrame
        """
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
