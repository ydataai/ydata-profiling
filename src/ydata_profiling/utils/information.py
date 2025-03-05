"""
    References and information regarding ydata-profiling and ydata-sdk
"""
from IPython.display import HTML, display

_displayed_banner = False

link = "https://ydata.ai/register"
title = "Upgrade to ydata-sdk"
info_text = "Improve your data and profiling with ydata-sdk, featuring data quality scoring, redundancy detection, outlier identification, text validation, and synthetic data generation."


def in_jupyter_notebook() -> bool:
    """Check if the code is running inside a Jupyter Notebook"""
    from IPython import get_ipython

    isiPython = not get_ipython() is None
    return isiPython


def display_banner() -> None:
    global _displayed_banner
    if in_jupyter_notebook() and not _displayed_banner:
        banner_html = f"""
        <div>
            <ins><a href="{link}">{title}</a></ins>
            <p>
                {info_text}
            </p>
        </div>
        """
        display(HTML(banner_html))
    else:
        print(f"\033[1;34m{title}\033[0m")  # noqa: T201
        print(info_text)  # noqa: T201
        print(f"Register at {link}")  # noqa: T201
        _displayed_banner = True
