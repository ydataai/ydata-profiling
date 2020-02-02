"""Generate the report."""
from datetime import datetime

import pandas_profiling.visualisation.plot as plot
from pandas_profiling.config import config
from pandas_profiling.model.base import (
    Boolean,
    Real,
    Count,
    Complex,
    Date,
    Categorical,
    Url,
    AbsolutePath,
    ExistingPath,
    ImagePath,
    Generic,
)
from pandas_profiling.model.messages import MessageType
from pandas_profiling.report.structure.variables import (
    render_boolean,
    render_categorical,
    render_complex,
    render_date,
    render_real,
    render_path,
    render_path_image,
    render_url,
    render_generic,
)
from pandas_profiling.report.presentation.abstract.renderable import Renderable
from pandas_profiling.report.presentation.core import (
    HTML,
    Image,
    Preview,
    Sequence,
    Overview,
    Dataset,
    Sample,
)


def get_missing_items(summary) -> list:
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


def get_correlation_items(summary) -> list:
    """Create the list of correlation items

    Args:
        summary: dict of correlations

    Returns:
        List of correlation items to show in the interface.
    """
    items = []

    key_to_data = {
        "pearson": (-1, "Pearson's r"),
        "spearman": (-1, "Spearman's ρ"),
        "kendall": (-1, "Kendall's τ"),
        "phi_k": (0, "Phik (φk)"),
        "cramers": (0, "Cramér's V (φc)"),
        "recoded": (0, "Recoded"),
    }

    image_format = config["plot"]["image_format"].get(str)

    for key, item in summary["correlations"].items():
        vmin, name = key_to_data[key]
        items.append(
            Image(
                plot.correlation_matrix(item, vmin=vmin),
                image_format=image_format,
                alt=name,
                anchor_id=key,
                name=name,
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
        ExistingPath: render_path,
        # ImagePath: render_path_image,
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

        template_variables = {
            "varname": idx,
            "varid": hash(idx),
            "warnings": warnings,
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

        templs.append(
            Preview(
                template_variables["top"],
                template_variables["bottom"],
                anchor_id=template_variables["varid"],
                name=idx,
                ignore=ignore,
            )
        )

    return templs


def get_sample_items(sample: dict):
    """Create the list of sample items

    Args:
        sample: dict of samples

    Returns:
        List of sample items to show in the interface.
    """
    items = []
    names = {"head": "First rows", "tail": "Last rows"}
    for key, value in sample.items():
        items.append(
            Sample(
                sample=value.to_html(classes="sample table table-striped"),
                name=names[key],
                anchor_id=key,
            )
        )
    return items


def get_scatter_matrix(scatter_matrix):
    image_format = config["plot"]["image_format"].get(str)

    titems = []
    for x_col, y_cols in scatter_matrix.items():
        items = []
        for y_col, splot in y_cols.items():
            items.append(
                Image(
                    splot,
                    image_format=image_format,
                    alt="{x_col} x {y_col}".format(x_col=x_col, y_col=y_col),
                    anchor_id="interactions_{x_col}_{y_col}".format(
                        x_col=x_col, y_col=y_col
                    ),
                    name="{y_col}".format(x_col=x_col, y_col=y_col),
                )
            )

        titems.append(
            Sequence(
                items,
                sequence_type="tabs",
                name=x_col,
                anchor_id="interactions_{x_col}".format(x_col=x_col),
            )
        )
    return titems


def get_report_structure(
    date_start: datetime, date_end: datetime, sample: dict, summary: dict
) -> Renderable:
    """Generate a HTML report from summary statistics and a given sample.

    Args:
      sample: A dict containing the samples to print.
      summary: Statistics to use for the overview, variables, correlations and missing values.

    Returns:
      The profile report in HTML format
    """

    scatter = Sequence(
        get_scatter_matrix(summary["scatter"]),
        sequence_type="tabs",
        name="Interactions",
        anchor_id="interactions",
    )
    collapse_warnings = config["warnings"]["collapse_if_more"].get(int)
    if collapse_warnings == 0:
        warnings = []
    else:
        warnings = summary["messages"]

    sections = Sequence(
        [
            Dataset(
                package=summary["package"],
                date_start=date_start,
                date_end=date_end,
                values=summary["table"],
                messages=warnings,
                collapse_warnings=len(warnings) > collapse_warnings,
                variables=summary["variables"],
                name="Overview",
                anchor_id="overview",
            ),
            Sequence(
                render_variables_section(summary),
                sequence_type="accordion",
                name="Variables",
                anchor_id="variables",
            ),
            scatter,
            Sequence(
                get_correlation_items(summary),
                sequence_type="tabs",
                name="Correlations",
                anchor_id="correlations",
            ),
            Sequence(
                get_missing_items(summary),
                sequence_type="tabs",
                name="Missing values",
                anchor_id="missing",
            ),
            Sequence(
                get_sample_items(sample),
                sequence_type="list",
                name="Sample",
                anchor_id="sample",
            ),
        ],
        name="Report",
        sequence_type="sections",
    )

    return sections
