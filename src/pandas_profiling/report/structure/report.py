"""Generate the report."""
import re
from typing import List

import pandas as pd
from tqdm.auto import tqdm

from pandas_profiling.config import config
from pandas_profiling.model.base import (
    AbsolutePath,
    Boolean,
    Categorical,
    Complex,
    Count,
    Date,
    FilePath,
    Generic,
    ImagePath,
    Real,
    Url,
)
from pandas_profiling.model.messages import MessageType
from pandas_profiling.report.presentation.core import (
    HTML,
    Collapse,
    Container,
    Duplicate,
    Image,
    Sample,
    ToggleButton,
    Variable,
)
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.report.presentation.core.root import Root
from pandas_profiling.report.structure.correlations import get_correlation_items
from pandas_profiling.report.structure.overview import get_dataset_items
from pandas_profiling.report.structure.variables import (
    render_boolean,
    render_categorical,
    render_complex,
    render_date,
    render_generic,
    render_image,
    render_path,
    render_real,
    render_url,
)
from pandas_profiling.report.structure.variables.render_file import render_file


def get_missing_items(summary) -> list:
    """Return the missing diagrams

    Args:
        summary: the dataframe summary

    Returns:
        A list with the missing diagrams
    """
    image_format = config["plot"]["image_format"].get(str)
    items = []
    for key, item in summary["missing"].items():
        items.append(
            # TODO: Add informative caption
            Image(
                item["matrix"],
                image_format=image_format,
                alt=item["name"],
                name=item["name"],
                anchor_id=key,
            )
        )

    return items


# TODO: split in per variable function
def render_variables_section(dataframe_summary: dict) -> list:
    """Render the HTML for each of the variables in the DataFrame.

    Args:
        dataframe_summary: The statistics for each variable.

    Returns:
        The rendered HTML, where each row represents a variable.
    """
    type_to_func = {
        Boolean: render_boolean,
        Real: render_real,
        Count: render_real,
        Complex: render_complex,
        Date: render_date,
        Categorical: render_categorical,
        Url: render_url,
        AbsolutePath: render_path,
        FilePath: render_file,
        ImagePath: render_image,
        Generic: render_generic,
    }

    templs = []

    for idx, summary in dataframe_summary["variables"].items():
        # Common template variables
        warnings = [
            warning.fmt()
            for warning in dataframe_summary["messages"]
            if warning.column_name == idx
        ]

        warning_fields = {
            field
            for warning in dataframe_summary["messages"]
            if warning.column_name == idx
            for field in warning.fields
        }

        warning_types = {
            warning.message_type
            for warning in dataframe_summary["messages"]
            if warning.column_name == idx
        }

        descriptions = config["variables"]["descriptions"].get(dict)
        show_description = config["show_variable_description"].get(bool)

        template_variables = {
            "varname": idx,
            "varid": hash(idx),
            "warnings": warnings,
            "description": descriptions.get(idx, "") if show_description else "",
            "warn_fields": warning_fields,
        }

        template_variables.update(summary)

        # Per type template variables
        template_variables.update(type_to_func[summary["type"]](template_variables))

        # Ignore these
        if config["reject_variables"].get(bool):
            ignore = MessageType.REJECTED in warning_types
        else:
            ignore = False

        bottom = None
        if "bottom" in template_variables and template_variables["bottom"] is not None:
            btn = ToggleButton("Toggle details", anchor_id=template_variables["varid"])
            bottom = Collapse(btn, template_variables["bottom"])

        var = Variable(
            template_variables["top"],
            bottom=bottom,
            anchor_id=template_variables["varid"],
            name=idx,
            ignore=ignore,
        )

        templs.append(var)

    return templs


def get_duplicates_items(duplicates: pd.DataFrame):
    """Create the list of duplicates items

    Args:
        duplicates: DataFrame of duplicates

    Returns:
        List of duplicates items to show in the interface.
    """
    items = []
    if duplicates is not None and len(duplicates) > 0:
        items.append(
            Duplicate(
                duplicate=duplicates,
                name="Most frequent",
                anchor_id="duplicates",
            )
        )
    return items


def get_definition_items(definitions: pd.DataFrame):
    """Create the list of duplicates items

    Args:
        definitions: DataFrame of column definitions

    Returns:
        List of column definitions to show in the interface.
    """
    items = []
    if definitions is not None and len(definitions) > 0:
        items.append(
            Duplicate(
                duplicate=definitions,
                name="Columns",
                anchor_id="definitions",
            )
        )
    return items


def get_sample_items(sample: dict):
    """Create the list of sample items

    Args:
        sample: dict of samples

    Returns:
        List of sample items to show in the interface.
    """
    items = []
    for obj in sample:
        items.append(
            Sample(
                sample=obj.data, name=obj.name, anchor_id=obj.id, caption=obj.caption
            )
        )
    return items


def get_scatter_matrix(scatter_matrix: dict) -> list:
    """Returns the interaction components for the report

    Args:
        scatter_matrix: a nested dict containing the scatter plots

    Returns:
        A list of components for the interaction section of the report
    """
    image_format = config["plot"]["image_format"].get(str)

    titems = []

    alphanum = re.compile("[^a-zA-Z\s]")

    def clean_name(name):
        return alphanum.sub("", name).replace(" ", "_")

    for x_col, y_cols in scatter_matrix.items():
        items = []
        for y_col, splot in y_cols.items():
            items.append(
                Image(
                    splot,
                    image_format=image_format,
                    alt=f"{x_col} x {y_col}",
                    anchor_id=f"interactions_{clean_name(x_col)}_{clean_name(y_col)}",
                    name=y_col,
                )
            )

        titems.append(
            Container(
                items,
                sequence_type="tabs" if len(items) <= 10 else "select",
                name=x_col,
                nested=len(scatter_matrix) > 10,
                anchor_id=f"interactions_{clean_name(x_col)}",
            )
        )
    return titems


def get_report_structure(summary: dict, sections: list = ["overview","variables","interactions","correlations","missing","sample","duplicate"]) -> Renderable:
    """Generate a HTML report from summary statistics and a given sample.

    Args:
      summary: Statistics to use for the overview, variables, correlations and missing values.

    Returns:
      The profile report in HTML format
    """
    disable_progress_bar = not config["progress_bar"].get(bool)
    with tqdm(
        total=1, desc="Generate report structure", disable=disable_progress_bar
    ) as pbar:
        warnings = summary["messages"]

        section_items: List[Renderable] = []

        if "overview" in sections:
            section_items.append(
                Container(
                    get_dataset_items(summary, warnings),
                    sequence_type="tabs",
                    name="Overview",
                    anchor_id="overview",
                )
            )

        if "variables" in sections:
            section_items.append(
                Container(
                    render_variables_section(summary),
                    sequence_type="accordion",
                    name="Variables",
                    anchor_id="variables",
                )
            )

        if "interactions" in sections:
            scatter_items = get_scatter_matrix(summary["scatter"])
            if len(scatter_items) > 0:
                section_items.append(
                    Container(
                        scatter_items,
                        sequence_type="tabs" if len(scatter_items) <= 10 else "select",
                        name="Interactions",
                        anchor_id="interactions",
                    ),
                )

        if "correlations" in sections:
            corr = get_correlation_items(summary)
            if corr is not None:
                section_items.append(corr)

        if "missing" in sections:
            missing_items = get_missing_items(summary)
            if len(missing_items) > 0:
                section_items.append(
                    Container(
                        missing_items,
                        sequence_type="tabs",
                        name="Missing values",
                        anchor_id="missing",
                    )
                )

        if "sample" in sections:
            sample_items = get_sample_items(summary["sample"])
            if len(sample_items) > 0:
                section_items.append(
                    Container(
                        items=sample_items,
                        sequence_type="list",
                        name="Sample",
                        anchor_id="sample",
                    )
                )

        if "duplicate" in sections:
            duplicate_items = get_duplicates_items(summary["duplicates"])
            if len(duplicate_items) > 0:
                section_items.append(
                    Container(
                        items=duplicate_items,
                        sequence_type="list",
                        name="Duplicate rows",
                        anchor_id="duplicate",
                    )
                )

        sections = Container(section_items, name="Root", sequence_type="sections")
        pbar.update()

    footer = HTML(
        content='Report generated with <a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling</a>.'
    )

    return Root("Root", sections, footer)
