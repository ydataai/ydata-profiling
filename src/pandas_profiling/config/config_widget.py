from typing import Union, Dict

import ipywidgets as widgets
from IPython.display import display

from pandas_profiling.utils.paths import get_config_buffer, get_config_default


def remove_useless_parameter(func):
    def wrapper(self, *args, **kwargs):
        return func(self)

    return wrapper


class ConfigParameter:
    hint_widget: widgets.HTML

    @classmethod
    def set_hint_widget(cls, hint):
        cls.hint_widget = hint

    def __init__(self, name, hint, widget):
        self.widget = widget
        self.name = name
        self.hint = hint
        self.observe()

    def observe(self):
        self.widget.observe(self.recall)

    def recall(self, content):
        ConfigWidget.config_buffer[self.name] = content.owner.value
        ConfigParameter.hint_widget.value = "[Hint] " + self.hint

    def display(self):
        display(self.widget)


class ConfigWidget:
    config_buffer: Dict[str, Union[bool, int, str]] = {}

    def __init__(self, profile_report):
        self.profile_report = profile_report
        self.hint_widget: widgets.HTML
        self.config_widget: widgets.VBox

    def build_widgets(self):
        layout = widgets.Layout(width="70%")
        style = {"description_width": "30%"}

        self.hint_widget = widgets.HTML("")
        ConfigParameter.set_hint_widget(self.hint_widget)

        all_config_parameter = {
            "title": ConfigParameter(
                "title",
                "Title for the report, shown in the header and title bar.",
                widgets.Text(
                    value=self.profile_report.config["title"].get(str),
                    placeholder="Profiling Report",
                    description="Report Title:",
                    layout=layout,
                    style=style,
                ),
            ),
            "multiprocess": ConfigParameter(
                "pool_size",
                "If True, pandas-profiling will parallel compute with all of your cores",
                widgets.Dropdown(
                    description="Multiprocess:",
                    options=[("True", 0), ("False", 1)],
                    label="True"
                    if self.profile_report.config["pool_size"].get(int) != 1
                    else "False",
                    layout=layout,
                    style=style,
                ),
            ),
            "progress_bar": ConfigParameter(
                "progress_bar",
                "If True, pandas-profiling will display a progress bar",
                widgets.Dropdown(
                    description="Progress bar:",
                    options=[("True", True), ("False", False)],
                    label=str(self.profile_report.config["progress_bar"]),
                    layout=layout,
                    style=style,
                ),
            ),
            "reject_variables": ConfigParameter(
                "reject_variables",
                "If True, pandas-profiling will auto reject variables",
                widgets.Dropdown(
                    description="Reject variables:",
                    options=[("True", True), ("False", False)],
                    label=str(self.profile_report.config["reject_variables"]),
                    layout=layout,
                    style=style,
                ),
            ),
            "skewness_threshold": ConfigParameter(
                "vars.num.skewness_threshold",
                "Warn if the skewness is above this threshold.",
                widgets.FloatText(
                    value=self.profile_report.config["vars"]["num"][
                        "skewness_threshold"
                    ].get(float),
                    description="Skewness:",
                    readout_format=".1f",
                    layout=layout,
                    style=style,
                ),
            ),
            "low_categorical_threshold": ConfigParameter(
                "vars.num.low_categorical_threshold",
                "If the number of distinct values is equal to or smaller than this number, then the series is "
                "considered to be categorical. Set to 0 to disable.",
                widgets.FloatText(
                    value=self.profile_report.config["vars"]["num"][
                        "low_categorical_threshold"
                    ].get(float),
                    description="Categorical:",
                    readout_format=".1f",
                    layout=layout,
                    style=style,
                ),
            ),
            "num_chi_squared_threshold": ConfigParameter(
                "vars.num.chi_squared_threshold",
                "Set to zero to disable chi squared calculation.",
                widgets.FloatText(
                    value=self.profile_report.config["vars"]["num"][
                        "chi_squared_threshold"
                    ].get(float),
                    description="Chi Squared:",
                    readout_format=".3f",
                    layout=layout,
                    style=style,
                ),
            ),
            "check_composition": ConfigParameter(
                "vars.cat.check_composition",
                "Check the character composition of the category/string. Informative, but may be "
                "computationally expensive.",
                widgets.Dropdown(
                    description="Check Composition:",
                    options=[("True", True), ("False", False)],
                    label=str(
                        self.profile_report.config["vars"]["cat"]["check_composition"]
                    ),
                    layout=layout,
                    style=style,
                ),
            ),
            "cardinality_threshold": ConfigParameter(
                "vars.cat.cardinality_threshold",
                "Warn if the number of distinct values is above this threshold.",
                widgets.FloatText(
                    value=self.profile_report.config["vars"]["cat"][
                        "cardinality_threshold"
                    ].get(float),
                    description="Cardinality:",
                    continuous_update=False,
                    readout_format=".1f",
                    layout=layout,
                    style=style,
                ),
            ),
            "cat_n_obs": ConfigParameter(
                "vars.cat.n_obs",
                "Display this number of observations.",
                widgets.BoundedIntText(
                    value=self.profile_report.config["vars"]["cat"]["n_obs"].get(float),
                    min=1,
                    max=50,
                    description="n_obs:",
                    readout_format="d",
                    layout=layout,
                    style=style,
                ),
            ),
            "cat_chi_squared_threshold": ConfigParameter(
                "vars.cat.chi_squared_threshold",
                "Set to zero to disable chi squared calculation.",
                widgets.FloatText(
                    value=self.profile_report.config["vars"]["cat"][
                        "chi_squared_threshold"
                    ].get(float),
                    step=0.001,
                    description="Chi Squared:",
                    readout_format=".3f",
                    layout=layout,
                    style=style,
                ),
            ),
            "bool_n_obs": ConfigParameter(
                "vars.bool.n_obs",
                "Display this number of observations.",
                widgets.BoundedIntText(
                    value=self.profile_report.config["vars"]["bool"]["n_obs"].get(int),
                    min=1,
                    max=50,
                    description="n_obs:",
                    readout_format="d",
                    layout=layout,
                    style=style,
                ),
            ),
            "sort": ConfigParameter(
                "sort",
                "Sort the variables asc(ending), desc(ending) or None (leaves original sorting).",
                widgets.Dropdown(
                    description="Sort:",
                    options=[
                        ("None", "None",),
                        ("Ascending", "Ascending"),
                        ("Descending", "Descending"),
                    ],
                    label=str(self.profile_report.config["sort"]),
                    layout=layout,
                    style=style,
                ),
            ),
            "mis_bar": ConfigParameter(
                "missing_diagrams.bar",
                "Display a bar chart with counts of missing values for each column.",
                widgets.Checkbox(
                    value=self.profile_report.config["missing_diagrams"]["bar"].get(
                        bool
                    ),
                    description="Bar",
                ),
            ),
            "mis_matrix": ConfigParameter(
                "missing_diagrams.matrix",
                "Display a matrix of missing values. Similar to the bar chart, but might provide overview of "
                "the co-occurrence of missing values in rows.",
                widgets.Checkbox(
                    value=self.profile_report.config["missing_diagrams"]["matrix"].get(
                        bool
                    ),
                    description="Matrix",
                ),
            ),
            "mis_heatmap": ConfigParameter(
                "missing_diagrams.heatmap",
                "Display a heatmap of missing values, that measures nullity correlation (i.e. how strongly "
                "the presence or absence of one variable affects the presence of another).",
                widgets.Checkbox(
                    value=self.profile_report.config["missing_diagrams"]["heatmap"].get(
                        bool
                    ),
                    description="Heatmap",
                ),
            ),
            "mis_dendrogram": ConfigParameter(
                "missing_diagrams.dendrogram",
                "Display a dendrogram. Provides insight in the co-occurrence of missing values (i.e. columns "
                "that are both filled or both none).",
                widgets.Checkbox(
                    value=self.profile_report.config["missing_diagrams"][
                        "dendrogram"
                    ].get(bool),
                    description="Dendrogram",
                ),
            ),
            "corr_pearson": ConfigParameter(
                "correlations.pearson.calculate",
                "Whether to calculate this coefficient",
                widgets.Checkbox(
                    value=self.profile_report.config["correlations"]["pearson"][
                        "calculate"
                    ].get(bool),
                    description="Pearson",
                ),
            ),
            "corr_spearman": ConfigParameter(
                "correlations.spearman.calculate",
                "Whether to calculate this coefficient",
                widgets.Checkbox(
                    value=self.profile_report.config["correlations"]["spearman"][
                        "calculate"
                    ].get(bool),
                    description="Spearman",
                ),
            ),
            "corr_kendall": ConfigParameter(
                "correlations.kendall.calculate",
                "Whether to calculate this coefficient",
                widgets.Checkbox(
                    value=self.profile_report.config["correlations"]["kendall"][
                        "calculate"
                    ].get(bool),
                    description="Kendall",
                ),
            ),
            "corr_phi_k": ConfigParameter(
                "correlations.phi_k.calculate",
                "Whether to calculate this coefficient",
                widgets.Checkbox(
                    value=self.profile_report.config["correlations"]["phi_k"][
                        "calculate"
                    ].get(bool),
                    description="Phi_k",
                ),
            ),
            "corr_cramers": ConfigParameter(
                "correlations.cramers.calculate",
                "Whether to calculate this coefficient",
                widgets.Checkbox(
                    value=self.profile_report.config["correlations"]["cramers"][
                        "calculate"
                    ].get(bool),
                    description="Cramers",
                ),
            ),
            "categorical_maximum_correlation_distinct": ConfigParameter(
                "categorical_maximum_correlation_distinct",
                "",
                widgets.IntText(
                    value=self.profile_report.config[
                        "categorical_maximum_correlation_distinct"
                    ].get(int),
                    description="Maximum Correlation Distinct:",
                    continuous_update=False,
                    orientation="horizontal",
                    readout=True,
                    readout_format="d",
                    layout=layout,
                    style=style,
                ),
            ),
            "interactions": ConfigParameter(
                "interactions.continuous",
                "Generate a 2D scatter plot (or hexagonal binned plot) for all continuous variable pairs.",
                widgets.Dropdown(
                    description="Interactions:",
                    options=[("True", True), ("False", False)],
                    label=str(self.profile_report.config["interactions"]["continuous"]),
                    layout=layout,
                    style=style,
                ),
            ),
            "image_format": ConfigParameter(
                "plot.image_format",
                "The format of generated images",
                widgets.Dropdown(
                    description="Image format:",
                    options=[("svg", "svg"), ("png", "png")],
                    label=self.profile_report.config["plot"]["image_format"].get(str),
                    layout=layout,
                    style=style,
                ),
            ),
            "dpi": ConfigParameter(
                "plot.dpi",
                "The dpi of generated images",
                widgets.IntText(
                    value=self.profile_report.config["plot"]["dpi"].get(int),
                    description="Image dpi:",
                    continuous_update=False,
                    orientation="horizontal",
                    readout=True,
                    readout_format="d",
                    layout=layout,
                    style=style,
                ),
            ),
            "histogram": ConfigParameter(
                "plot.histogram.bins",
                "The number of histogram bins",
                widgets.BoundedIntText(
                    value=self.profile_report.config["plot"]["histogram"]["bins"].get(
                        int
                    ),
                    min=1,
                    max=1000,
                    description="No.Histogram Bins:",
                    continuous_update=False,
                    orientation="horizontal",
                    readout=True,
                    readout_format="d",
                    layout=layout,
                    style=style,
                ),
            ),
            "primary_color": ConfigParameter(
                "html.style.primary_color",
                "The primary color of html report",
                widgets.ColorPicker(
                    concise=False,
                    description="Primary Color",
                    value=self.profile_report.config["html"]["style"][
                        "primary_color"
                    ].get(str),
                    disabled=False,
                    layout=layout,
                    style=style,
                ),
            ),
        }

        def get_widgets(keys):
            return [all_config_parameter[a].widget for a in keys.split(",")]

        basic_config = widgets.VBox(
            get_widgets("title,multiprocess,progress_bar,interactions,primary_color")
        )

        # variable config parameters
        variable = widgets.Tab(
            children=[
                widgets.VBox(
                    get_widgets(
                        "skewness_threshold,low_categorical_threshold,num_chi_squared_threshold"
                    )
                ),
                widgets.VBox(
                    get_widgets(
                        "check_composition,cardinality_threshold,cat_n_obs,cat_chi_squared_threshold"
                    )
                ),
                widgets.VBox(get_widgets("bool_n_obs")),
                widgets.VBox(
                    get_widgets("mis_bar,mis_matrix,mis_heatmap,mis_dendrogram")
                ),
                widgets.VBox(
                    get_widgets(
                        "corr_pearson,corr_spearman,corr_kendall,corr_phi_k,corr_cramers"
                    )
                ),
                widgets.VBox(
                    get_widgets("sort,categorical_maximum_correlation_distinct")
                ),
            ]
        )

        variable.set_title(0, "Numeric")
        variable.set_title(1, "Catgory")
        variable.set_title(2, "Boolen")
        variable.set_title(3, "Missing Diagrams")
        variable.set_title(4, "Correlations")
        variable.set_title(5, "Misc")

        # plot config parameters
        plot = widgets.VBox(get_widgets("image_format,dpi,histogram"))

        # all config parameters
        accordion = widgets.Accordion(children=[basic_config, variable, plot])

        accordion.set_title(0, "Overview")
        accordion.set_title(1, "Variable Stat")
        accordion.set_title(2, "Plot")

        # confirm button
        confirm_button = widgets.Button(
            description="Confirm", disabled=False, button_style="success", icon="check",
        )
        confirm_button.on_click(self._set_config)

        # upload config button
        upload_config = widgets.FileUpload(
            accept=".yaml",
            button_style="info",
            multiple=False,
            description="Upload config",
        )

        # download config button
        download_config = widgets.Button(
            description="Download config",
            disabled=False,
            button_style="info",
            icon="download",
        )
        download_config.on_click(self.download)

        # restore button
        restore_button = widgets.Button(
            description="Restore default",
            disabled=False,
            button_style="warning",
            icon="check",
        )

        # refresh button
        refresh_button = widgets.Button(
            description="Refresh",
            disabled=False,
            button_style="warning",
            icon="refresh",
        )

        # close button
        close_button = widgets.Button(
            description="Close", disabled=False, button_style="danger", icon="close",
        )

        # full widget
        self.config_widget = widgets.VBox(
            [
                accordion,
                widgets.VBox(
                    [
                        self.hint_widget,
                        widgets.HBox(
                            [
                                confirm_button,
                                upload_config,
                                download_config,
                                restore_button,
                                refresh_button,
                                close_button,
                            ]
                        ),
                    ]
                ),
            ]
        )
        restore_button.on_click(self.restore)
        close_button.on_click(self.close)
        refresh_button.on_click(self.refresh)
        upload_config.observe(self.set_upload_config)
        return self.config_widget

    @remove_useless_parameter
    def restore(self):
        ConfigWidget.config_buffer.clear()
        self.profile_report.config.set_file(str(get_config_default()))
        self.refresh()

    @remove_useless_parameter
    def display(self):
        display(self.build_widgets())

    @remove_useless_parameter
    def refresh(self):
        self.close()
        ConfigWidget.config_buffer.clear()
        self.display()

    @remove_useless_parameter
    def close(self):
        ConfigWidget.config_buffer.clear()
        self.config_widget.close_all()

    @remove_useless_parameter
    def download(self):
        # TODO: implement the download logic
        self.hint_widget.value = f"<a download=config.yaml href='data:text/plain;charset=utf-8,{self.profile_report.config.dump()}'>Click here to download</a>"

    @remove_useless_parameter
    def _set_config(self):
        # TODO: Do a.b.c=v => {a:{b:{c:v}} more elegant
        variables = {}
        for key, v in ConfigWidget.config_buffer.items():
            keys = key.split(".")
            if len(keys) == 3:
                variables.setdefault(keys[0], {})
                variables[keys[0]].setdefault(keys[1], {})
                variables[keys[0]][keys[1]][keys[2]] = v
            elif len(keys) == 2:
                variables.setdefault(keys[0], {})
                variables[keys[0]][keys[1]] = v
            elif len(keys) == 1:
                variables[keys[0]] = v

        self.profile_report.set_variables(**variables)
        self.hint_widget.value = "The configuration item was updated successfully"
        ConfigWidget.config_buffer.clear()

    def set_upload_config(self, content):
        try:
            data = content["new"]["data"][0].tobytes()
        except:
            return
        try:
            buffer_config = str(get_config_buffer())
            with open(buffer_config, "wb") as f:
                f.write(data)
            self.profile_report.config.set_file(buffer_config)
        except Exception as e:
            raise ValueError(f"Failed to load the upload Config file:{e}")

        self.close()
