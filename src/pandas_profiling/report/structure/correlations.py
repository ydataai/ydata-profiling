from typing import List, Optional

from pandas_profiling.config import Settings
from pandas_profiling.report.presentation.core import (
    HTML,
    Collapse,
    Container,
    Image,
    ToggleButton,
)
from pandas_profiling.report.presentation.core.renderable import Renderable
from pandas_profiling.visualisation import plot


def get_correlation_items(config: Settings, summary: dict) -> Optional[Renderable]:
    """Create the list of correlation items

    Args:
        config: report Settings object
        summary: dict of correlations

    Returns:
        List of correlation items to show in the interface.
    """
    items: List[Renderable] = []

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

    phi_k_description = """Phik (φk) is a new and practical correlation coefficient that works consistently between categorical, ordinal and interval variables, captures non-linear dependency and reverts to the Pearson correlation coefficient in case
    of a bivariate normal input distribution. There is extensive documentation available <a href='https://phik.readthedocs.io/en/latest/index.html'>here</a>."""

    cramers_description = """Cramér's V is an association measure for nominal random variables. The coefficient ranges from 0 to 1, with 0 indicating independence and 1 indicating perfect association.
    The empirical estimators used for Cramér's V have been proved to be biased, even for large samples.
    We use a bias-corrected measure that has been proposed by Bergsma in 2013 that can be found <a href='http://stats.lse.ac.uk/bergsma/pdf/cramerV3.pdf'>here</a>."""

    key_to_data = {
        "pearson": (-1, "Pearson's r", pearson_description),
        "spearman": (-1, "Spearman's ρ", spearman_description),
        "kendall": (-1, "Kendall's τ", kendall_description),
        "phi_k": (0, "Phik (φk)", phi_k_description),
        "cramers": (0, "Cramér's V (φc)", cramers_description),
    }

    image_format = config.plot.image_format

    for key, item in summary["correlations"].items():
        vmin, name, description = key_to_data[key]

        diagram = Image(
            plot.correlation_matrix(config, item, vmin=vmin),
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

            tbl = Container(
                [diagram, desc], anchor_id=key, name=name, sequence_type="grid"
            )

            items.append(tbl)
        else:
            items.append(diagram)

    corr = Container(
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
