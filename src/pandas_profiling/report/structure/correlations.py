from typing import Optional, List

from pandas_profiling.config import config
from pandas_profiling.report.presentation.abstract.renderable import Renderable
from pandas_profiling.report.presentation.core import (
    Sequence,
    HTML,
    Image,
    ToggleButton,
    Collapse,
)
from pandas_profiling.visualisation import plot


def get_items() -> List[Renderable]:
    return []


def get_correlation_items(summary) -> Optional[Renderable]:
    """Create the list of correlation items

    Args:
        summary: dict of correlations

    Returns:
        List of correlation items to show in the interface.
    """
    items = get_items()

    pearson_description = (
        "The Pearson's correlation coefficient (<em>r</em>) is a measure of linear correlation "
        "between two variables. It's value lies between -1 and +1, -1 indicating total negative "
        "linear correlation, 0 indicating no linear correlation and 1 indicating total positive "
        "linear correlation. Furthermore, <em>r</em> is invariant under separate changes in location "
        "and scale of the two variables, implying that for a linear function the angle to the "
        "x-axis does not affect <em>r</em>.<br /><br />To calculate <em>r</em> for two "
        "variables <em>X</em> and <em>Y</em>, one divides the covariance of <em>X</em> and "
        "<em>Y</em> by the product of their standard deviations. "
    )
    spearman_description = """The Spearman's rank correlation coefficient (<em>ρ</em>) is a measure of monotonic 
    correlation between two variables, and is therefore better in catching nonlinear monotonic correlations than 
    Pearson's <em>r</em>. It's value lies between -1 and +1, -1 indicating total negative monotonic correlation, 
    0 indicating no monotonic correlation and 1 indicating total positive monotonic correlation.<br /><br />To 
    calculate <em>ρ</em> for two variables <em>X</em> and <em>Y</em>, one divides the covariance of the rank 
    variables of <em>X</em> and <em>Y</em> by the product of their standard deviations. """

    kendall_description = """Similarly to Spearman's rank correlation coefficient, the Kendall rank correlation 
    coefficient (<em>τ</em>) measures ordinal association between two variables. It's value lies between -1 and +1, 
    -1 indicating total negative correlation, 0 indicating no correlation and 1 indicating total positive correlation.
    <br /><br />To calculate <em>τ</em> for two variables <em>X</em> and <em>Y</em>, one determines the number of 
    concordant and discordant pairs of observations. <em>τ</em> is given by the number of concordant pairs minus the 
    discordant pairs divided by the total number of pairs."""

    key_to_data = {
        "pearson": (-1, "Pearson's r", pearson_description),
        "spearman": (-1, "Spearman's ρ", spearman_description),
        "kendall": (-1, "Kendall's τ", kendall_description),
        "phi_k": (0, "Phik (φk)", ""),
        "cramers": (0, "Cramér's V (φc)", ""),
        "recoded": (0, "Recoded", ""),
    }

    image_format = config["plot"]["image_format"].get(str)

    for key, item in summary["correlations"].items():
        vmin, name, description = key_to_data[key]

        diagram = Image(
            plot.correlation_matrix(item, vmin=vmin),
            image_format=image_format,
            alt=name,
            anchor_id=f"{key}_diagram",
            name=name,
            classes="correlation-diagram",
        )

        if len(description) > 0:
            desc = HTML(
                f'<div style="padding:20px" class="text-muted"><h3>{name}</h3>{description}</div>',
                anchor_id=f"{key}_html",
                classes="correlation-description",
            )

            tbl = Sequence(
                [diagram, desc], anchor_id=key, name=name, sequence_type="grid"
            )

            items.append(tbl)
        else:
            items.append(diagram)

    corr = Sequence(
        items,
        sequence_type="tabs",
        name="Correlations Tab",
        anchor_id="correlations_tab",
    )

    if len(items) > 0:
        btn = ToggleButton(
            "Toggle correlation descriptions",
            anchor_id="toggle-correlation-description",
            name="Toggle correlation descriptions",
        )

        return Collapse(
            name="Correlations", anchor_id="correlations", button=btn, item=corr
        )
    else:
        return None
