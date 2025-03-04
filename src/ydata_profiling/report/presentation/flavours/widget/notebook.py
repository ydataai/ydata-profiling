"""Functionality related to displaying the profile report in Jupyter notebooks."""
import html
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from IPython.display import HTML
    from IPython.lib.display import IFrame

from ydata_profiling import ProfileReport
from ydata_profiling.config import IframeAttribute, Settings


def get_notebook_iframe_srcdoc(config: Settings, profile: ProfileReport) -> "HTML":
    """Get the IPython HTML object with iframe with the srcdoc attribute

    Args:
        config: Settings
        profile: The profile report object

    Returns:
        IPython HTML object.
    """
    from IPython.display import HTML

    width = config.notebook.iframe.width
    height = config.notebook.iframe.height
    src = html.escape(profile.to_html())

    iframe = f'<iframe width="{width}" height="{height}" srcdoc="{src}" frameborder="0" allowfullscreen></iframe>'

    return HTML(iframe)


def get_notebook_iframe_src(config: Settings, profile: ProfileReport) -> "IFrame":
    """Get the IPython IFrame object

    Args:
        config: Settings
        profile: The profile report object

    Returns:
        IPython IFrame object.
    """
    tmp_file = Path("./ipynb_tmp") / f"{uuid.uuid4().hex}.html"
    tmp_file.parent.mkdir(exist_ok=True)
    profile.to_file(tmp_file)
    from IPython.lib.display import IFrame

    return IFrame(
        str(tmp_file),
        width=config.notebook.iframe.width,
        height=config.notebook.iframe.height,
    )


def get_notebook_iframe(
    config: Settings, profile: ProfileReport
) -> Union["IFrame", "HTML"]:
    """Display the profile report in an iframe in the Jupyter notebook

    Args:
        config: Settings
        profile: The profile report object

    Returns:
        Displays the Iframe
    """

    attribute = config.notebook.iframe.attribute
    if attribute == IframeAttribute.src:
        output = get_notebook_iframe_src(config, profile)
    elif attribute == IframeAttribute.srcdoc:
        output = get_notebook_iframe_srcdoc(config, profile)
    else:
        raise ValueError(
            f'Iframe Attribute can be "src" or "srcdoc" (current: {attribute}).'
        )

    return output
