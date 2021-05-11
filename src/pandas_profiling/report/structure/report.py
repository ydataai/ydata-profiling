"""Generate the report."""
from typing import List, Sequence

import pandas as pd
from tqdm.auto import tqdm

from pandas_profiling.config import Settings
from pandas_profiling.model.handler import get_render_map
from pandas_profiling.model.messages import MessageType
from pandas_profiling.report.presentation.core import (
    HTML,
    Collapse,
    Container,
    Duplicate,
)
from pandas_profiling.report.presentation.core import Image as ImageWidget
from pandas_profiling.report.presentation.core import Sample, ToggleButton, Variable
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.report.presentation.core.root import Root
from pandas_profiling.report.structure.correlations import get_correlation_items
from pandas_profiling.report.structure.overview import get_dataset_items
from pandas_profiling.utils.dataframe import slugify


def get_missing_items(config: Settings, summary: dict) -> list:
    """Return the missing diagrams

    Args:
        config: report Settings object
        summary: the dataframe summary

    Returns:
        A list with the missing diagrams
    """
    items = [
        ImageWidget(
            item["matrix"],
            image_format=config.plot.image_format,
            alt=item["name"],
            name=item["name"],
            anchor_id=key,
            caption=item["caption"],
        )
        for key, item in summary["missing"].items()
    ]

    return items


def render_variables_section(config: Settings, dataframe_summary: dict) -> list:
    """Render the HTML for each of the variables in the DataFrame.

    Args:
        config: report Settings object
        dataframe_summary: The statistics for each variable.

    Returns:
        The rendered HTML, where each row represents a variable.
    """

    templs = []

    descriptions = config.variables.descriptions
    show_description = config.show_variable_description
    reject_variables = config.reject_variables

    render_map = get_render_map()

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

        template_variables = {
            "varname": idx,
            "varid": hash(idx),
            "warnings": warnings,
            "description": descriptions.get(idx, "") if show_description else "",
            "warn_fields": warning_fields,
        }

        template_variables.update(summary)

        # Per type template variables
        template_variables.update(
            render_map[summary["type"]](config, template_variables)
        )

        # Ignore these
        if reject_variables:
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


def get_duplicates_items(duplicates: pd.DataFrame) -> Sequence[Renderable]:
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
                name="Most frequently occurring",
                anchor_id="duplicates",
            )
        )
    return items


def get_definition_items(definitions: pd.DataFrame) -> Sequence[Renderable]:
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


def get_sample_items(sample: dict) -> List[Sample]:
    """Create the list of sample items

    Args:
        sample: dict of samples

    Returns:
        List of sample items to show in the interface.
    """
    items = [
        Sample(sample=obj.data, name=obj.name, anchor_id=obj.id, caption=obj.caption)
        for obj in sample
    ]
    return items


def get_scatter_matrix(config: Settings, scatter_matrix: dict) -> list:
    """Returns the interaction components for the report

    Args:
        scatter_matrix: a nested dict containing the scatter plots

    Returns:
        A list of components for the interaction section of the report
    """
    titems = []

    for x_col, y_cols in scatter_matrix.items():
        items = [
            ImageWidget(
                splot,
                image_format=config.plot.image_format,
                alt=f"{x_col} x {y_col}",
                anchor_id=f"interactions_{slugify(x_col)}_{slugify(y_col)}",
                name=y_col,
            )
            for y_col, splot in y_cols.items()
        ]

        titems.append(
            Container(
                items,
                sequence_type="tabs" if len(items) <= 10 else "select",
                name=x_col,
                nested=len(scatter_matrix) > 10,
                anchor_id=f"interactions_{slugify(x_col)}",
            )
        )
    return titems


def get_report_structure(config: Settings, summary: dict) -> Root:
    """Generate a HTML report from summary statistics and a given sample.

    Args:
      config: report Settings object
      summary: Statistics to use for the overview, variables, correlations and missing values.

    Returns:
      The profile report in HTML format
    """
    disable_progress_bar = not config.progress_bar
    with tqdm(
        total=1, desc="Generate report structure", disable=disable_progress_bar
    ) as pbar:
        warnings = summary["messages"]

        section_items: List[Renderable] = [
            Container(
                get_dataset_items(config, summary, warnings),
                sequence_type="tabs",
                name="Overview",
                anchor_id="overview",
            ),
            Container(
                render_variables_section(config, summary),
                sequence_type="accordion",
                name="Variables",
                anchor_id="variables",
            ),
        ]

        scatter_items = get_scatter_matrix(config, summary["scatter"])
        if len(scatter_items) > 0:
            section_items.append(
                Container(
                    scatter_items,
                    sequence_type="tabs" if len(scatter_items) <= 10 else "select",
                    name="Interactions",
                    anchor_id="interactions",
                ),
            )

        corr = get_correlation_items(config, summary)
        if corr is not None:
            section_items.append(corr)

        missing_items = get_missing_items(config, summary)
        if len(missing_items) > 0:
            section_items.append(
                Container(
                    missing_items,
                    sequence_type="tabs",
                    name="Missing values",
                    anchor_id="missing",
                )
            )

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

        sections = Container(
            section_items,
            name="Root",
            sequence_type="sections",
            full_width=config.html.full_width,
        )
        pbar.update()

    footer = HTML(
        content='Report generated with <a href="https://github.com/pandas-profiling/pandas-profiling">pandas-profiling</a>.'
    )

    return Root("Root", sections, footer)
