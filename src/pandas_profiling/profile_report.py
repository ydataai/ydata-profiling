import copy
import json
import warnings
from pathlib import Path
from typing import Any, Dict, Optional, Union

import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from typeguard import typechecked
from visions import VisionsTypeset

from pandas_profiling.config import Config, Settings
from pandas_profiling.expectations_report import ExpectationsReport
from pandas_profiling.model.alerts import AlertType
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.model.sample import Sample
from pandas_profiling.model.summarizer import (
    BaseSummarizer,
    PandasProfilingSummarizer,
    format_summary,
)
from pandas_profiling.model.typeset import ProfilingTypeSet
from pandas_profiling.report import get_report_structure
from pandas_profiling.report.presentation.core import Root
from pandas_profiling.report.presentation.flavours.html.templates import (
    create_html_assets,
)
from pandas_profiling.serialize_report import SerializeReport
from pandas_profiling.utils.dataframe import hash_dataframe
from pandas_profiling.utils.paths import get_config


@typechecked
class ProfileReport(SerializeReport, ExpectationsReport):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.

    Used as is, it will output its content as an HTML report in a Jupyter notebook.
    """

    _description_set = None
    _report = None
    _html = None
    _widgets = None
    _json = None
    config: Settings

    def __init__(
        self,
        df: Optional[pd.DataFrame] = None,
        minimal: bool = False,
        explorative: bool = False,
        sensitive: bool = False,
        dark_mode: bool = False,
        orange_mode: bool = False,
        tsmode: bool = False,
        sortby: Optional[str] = None,
        sample: Optional[dict] = None,
        config_file: Union[Path, str] = None,
        lazy: bool = True,
        typeset: Optional[VisionsTypeset] = None,
        summarizer: Optional[BaseSummarizer] = None,
        config: Optional[Settings] = None,
        **kwargs,
    ):
        """Generate a ProfileReport based on a pandas DataFrame

        Config processing order (in case of duplicate entries, entries later in the order are retained):
        - config presets (e.g. `config_file`, `minimal` arguments)
        - config groups (e.g. `explorative` and `sensitive` arguments)
        - custom settings (e.g. `config` argument)
        - custom settings **kwargs (e.g. `title`)

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

        if df is None and not lazy:
            raise ValueError("Can init a not-lazy ProfileReport with no DataFrame")

        if config_file is not None and minimal:
            raise ValueError(
                "Arguments `config_file` and `minimal` are mutually exclusive."
            )

        if config_file or minimal:
            if not config_file:
                config_file = get_config("config_minimal.yaml")

            report_config = Settings().from_file(config_file)
        else:
            report_config = Settings()

        groups = [
            (explorative, "explorative"),
            (sensitive, "sensitive"),
            (dark_mode, "dark_mode"),
            (orange_mode, "orange_mode"),
        ]
        if any(condition for condition, _ in groups):
            cfg = Settings()
            for condition, key in groups:
                if condition:
                    cfg = cfg.update(Config.get_arg_groups(key))
            report_config = cfg.update(report_config.dict(exclude_defaults=True))

        if len(kwargs) > 0:
            shorthands, kwargs = Config.shorthands(kwargs)
            report_config = (
                Settings()
                .update(shorthands)
                .update(report_config.dict(exclude_defaults=True))
            )

        if config is not None:
            report_config = report_config.update(config.dict())
            report_config.html.style._labels = config.html.style._labels

        if kwargs:
            report_config = report_config.update(kwargs)

        report_config.vars.timeseries.active = tsmode
        if tsmode and sortby:
            report_config.vars.timeseries.sortby = sortby

        self.df = self.__initialize_dataframe(df, report_config)
        self.config = report_config
        self._df_hash = None
        self._sample = sample
        self._typeset = typeset
        self._summarizer = summarizer

        if not lazy:
            # Trigger building the report structure
            _ = self.report

    @staticmethod
    def __initialize_dataframe(
        df: Optional[pd.DataFrame], report_config: Settings
    ) -> Optional[pd.DataFrame]:
        if (
            df is not None
            and report_config.vars.timeseries.active
            and report_config.vars.timeseries.sortby
        ):
            return df.sort_values(by=report_config.vars.timeseries.sortby).reset_index(
                drop=True
            )
        else:
            return df

    def invalidate_cache(self, subset: Optional[str] = None) -> None:
        """Invalidate report cache. Useful after changing setting.

        Args:
            subset:
            - "rendering" to invalidate the html, json and widget report rendering
            - "report" to remove the caching of the report structure
            - None (default) to invalidate all caches

        Returns:
            None
        """
        if subset is not None and subset not in ["rendering", "report"]:
            raise ValueError(
                "'subset' parameter should be None, 'rendering' or 'report'"
            )

        if subset is None or subset in ["rendering", "report"]:
            self._widgets = None
            self._json = None
            self._html = None

        if subset is None or subset == "report":
            self._report = None

        if subset is None:
            self._description_set = None

    @property
    def typeset(self) -> Optional[VisionsTypeset]:
        if self._typeset is None:
            self._typeset = ProfilingTypeSet(self.config)
        return self._typeset

    @property
    def summarizer(self) -> BaseSummarizer:
        if self._summarizer is None:
            self._summarizer = PandasProfilingSummarizer(self.typeset)
        return self._summarizer

    @property
    def description_set(self) -> Dict[str, Any]:
        if self._description_set is None:
            self._description_set = describe_df(
                self.config,
                self.df,
                self.summarizer,
                self.typeset,
                self._sample,
            )
        return self._description_set

    @property
    def df_hash(self) -> Optional[str]:
        if self._df_hash is None and self.df is not None:
            self._df_hash = hash_dataframe(self.df)
        return self._df_hash

    @property
    def report(self) -> Root:
        if self._report is None:
            self._report = get_report_structure(self.config, self.description_set)
        return self._report

    @property
    def html(self) -> str:
        if self._html is None:
            self._html = self._render_html()
        return self._html

    @property
    def json(self) -> str:
        if self._json is None:
            self._json = self._render_json()
        return self._json

    @property
    def widgets(self) -> Any:
        if (
            isinstance(self.description_set["table"]["n"], list)
            and len(self.description_set["table"]["n"]) > 1
        ):
            raise RuntimeError(
                "Widgets interface not (yet) supported for comparing reports, please use the HTML rendering."
            )

        if self._widgets is None:
            self._widgets = self._render_widgets()
        return self._widgets

    def get_duplicates(self) -> Optional[pd.DataFrame]:
        """Get duplicate rows and counts based on the configuration

        Returns:
            A DataFrame with the duplicate rows and their counts.
        """
        return self.description_set["duplicates"]

    def get_sample(self) -> dict:
        """Get head/tail samples based on the configuration

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
            alert.column_name
            for alert in self.description_set["alerts"]
            if alert.alert_type == AlertType.REJECTED
        }

    def to_file(self, output_file: Union[str, Path], silent: bool = True) -> None:
        """Write the report to a file.

        Args:
            output_file: The name or the path of the file to generate including the extension (.html, .json).
            silent: if False, opens the file in the default browser or download it in a Google Colab environment
        """
        if not isinstance(output_file, Path):
            output_file = Path(str(output_file))

        if output_file.suffix == ".json":
            data = self.to_json()
        else:
            if not self.config.html.inline:
                self.config.html.assets_path = str(output_file.parent)
                if self.config.html.assets_prefix is None:
                    self.config.html.assets_prefix = str(output_file.stem) + "_assets"
                create_html_assets(self.config, output_file)

            data = self.to_html()

            if output_file.suffix != ".html":
                suffix = output_file.suffix
                output_file = output_file.with_suffix(".html")
                warnings.warn(
                    f"Extension {suffix} not supported. For now we assume .html was intended. "
                    f"To remove this warning, please use .html or .json."
                )

        disable_progress_bar = not self.config.progress_bar
        with tqdm(
            total=1, desc="Export report to file", disable=disable_progress_bar
        ) as pbar:
            output_file.write_text(data, encoding="utf-8")
            pbar.update()

        if not silent:
            try:
                from google.colab import files  # noqa: F401

                files.download(output_file.absolute().as_uri())
            except ModuleNotFoundError:
                import webbrowser

                webbrowser.open_new_tab(output_file.absolute().as_uri())

    def _render_html(self) -> str:
        from pandas_profiling.report.presentation.flavours import HTMLReport

        report = self.report

        with tqdm(
            total=1, desc="Render HTML", disable=not self.config.progress_bar
        ) as pbar:
            html = HTMLReport(copy.deepcopy(report)).render(
                nav=self.config.html.navbar_show,
                offline=self.config.html.use_local_assets,
                inline=self.config.html.inline,
                assets_prefix=self.config.html.assets_prefix,
                primary_color=self.config.html.style.primary_colors[0],
                logo=self.config.html.style.logo,
                theme=self.config.html.style.theme,
                title=self.description_set["analysis"]["title"],
                date=self.description_set["analysis"]["date_start"],
                version=self.description_set["package"]["pandas_profiling_version"],
            )

            if self.config.html.minify_html:
                from htmlmin.main import minify

                html = minify(html, remove_all_empty_space=True, remove_comments=True)
            pbar.update()
        return html

    def _render_widgets(self) -> Any:
        from pandas_profiling.report.presentation.flavours import WidgetReport

        report = self.report

        with tqdm(
            total=1,
            desc="Render widgets",
            disable=not self.config.progress_bar,
            leave=False,
        ) as pbar:
            widgets = WidgetReport(copy.deepcopy(report)).render()
            pbar.update()
        return widgets

    def _render_json(self) -> str:
        def encode_it(o: Any) -> Any:
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
                    return encode_it(o.dict())
                elif isinstance(o, np.generic):
                    return o.item()
                else:
                    return str(o)

        description = self.description_set

        with tqdm(
            total=1, desc="Render JSON", disable=not self.config.progress_bar
        ) as pbar:
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

    def to_notebook_iframe(self) -> None:
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
            display(get_notebook_iframe(self.config, self))

    def to_widgets(self) -> None:
        """The ipython notebook widgets user interface."""
        try:
            from google.colab import files  # noqa: F401

            warnings.warn(
                "Ipywidgets is not yet fully supported on Google Colab (https://github.com/googlecolab/colabtools/issues/60)."
                "As an alternative, you can use the HTML report. See the documentation for more information."
            )
        except ModuleNotFoundError:
            pass

        from IPython.core.display import display

        display(self.widgets)

    def _repr_html_(self) -> None:
        """The ipython notebook widgets user interface gets called by the jupyter notebook."""
        self.to_notebook_iframe()

    def __repr__(self) -> str:
        """Override so that Jupyter Notebook does not print the object."""
        return ""

    def compare(
        self, other: "ProfileReport", config: Optional[Settings] = None
    ) -> "ProfileReport":
        """Compare this report with another ProfileReport
        Alias for:
        ```
        pandas_profiling.compare([report1, report2], config=config)
        ```
        See `pandas_profiling.compare` for details.

        Args:
            other: the ProfileReport to compare to
            config: the settings object for the merged ProfileReport. If `None`, uses the caller's config

        Returns:
            Comparison ProfileReport
        """
        from pandas_profiling.compare_reports import compare

        return compare([self, other], config if config is not None else self.config)
