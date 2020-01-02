"""Functionality related to displaying the profile report in Jupyter notebooks."""
import html
from pathlib import Path


from pandas_profiling.config import config


def get_notebook_iframe_srcdoc(profile):
    """Get the IPython HTML object with ifram with the srcdoc attribute

    Args:
        profile: The profile report object

    Returns:
        IPython HTML object.
    """
    from IPython.core.display import HTML

    iframe = """
                <iframe
                    width="{width}"
                    height="{height}"
                    srcdoc="{src}"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
                """
    iframe = iframe.format(
        width=config["notebook"]["iframe"]["width"].get(str),
        height=config["notebook"]["iframe"]["height"].get(str),
        src=html.escape(profile.to_html()),
    )
    return HTML(iframe)


def get_notebook_iframe_src(profile):
    """Get the IPython IFrame object

    Args:
        profile: The profile report object

    Returns:
        IPython IFrame object.
    """
    tmp_file = Path("./ipynb_tmp") / profile.get_unique_file_name()
    tmp_file.parent.mkdir(exist_ok=True)
    profile.to_file(tmp_file)
    from IPython.lib.display import IFrame

    return IFrame(
        str(tmp_file),
        width=config["notebook"]["iframe"]["width"].get(str),
        height=config["notebook"]["iframe"]["height"].get(str),
    )


def display_notebook_iframe(profile):
    """Display the profile report in an iframe in the Jupyter notebook

    Args:
        profile: The profile report object

    Returns:
        Displays the Iframe
    """
    from IPython.core.display import display

    attribute = config["notebook"]["iframe"]["attribute"].get(str)
    if attribute == "src":
        output = get_notebook_iframe_src(profile)
    elif attribute == "srcdoc":
        output = get_notebook_iframe_srcdoc(profile)
    else:
        raise ValueError(
            'Iframe Attribute can be "src" or "srcdoc" (current: {}).'.format(attribute)
        )

    display(output)
