"""
    References and information regarding ydata-profiling and ydata-sdk
"""
import importlib.util

_displayed_banner = False

link = "https://ydata.ai/register"
title = "Upgrade to ydata-sdk"
info_text = "Improve your data and profiling with ydata-sdk, featuring data quality scoring, redundancy detection, outlier identification, text validation, and synthetic data generation."


def in_jupyter_notebook() -> bool:
    """Check if the code is running inside a Jupyter Notebook"""
    if importlib.util.find_spec("IPython") is not None:
        from IPython import get_ipython

        isiPython = not get_ipython() is None
    else:
        isiPython = False
    return isiPython


class DisplayInfo:
    def __init__(
        self,
        title: str,
        info_text: str,
        link: str = "ttps://ydata.ai/register",
    ):
        self.title = title
        self.link = link
        self.info_text = info_text

    def display_message(self) -> None:
        """
        Display an HTML message in case the user is in a Jupyter Notebook
        """
        if in_jupyter_notebook():
            from IPython.display import HTML, display

            info = f"""
            <div>
                <ins><a href="{self.link}">{self.title}</a></ins>
                <p>
                    {self.info_text}
                </p>
            </div>
            """
            display(HTML(info))
        else:
            info = (
                f"\033[1;34m{self.title}\033[0m"
                + "\n"
                + f"{self.info_text}"
                + "\n"
                + f"Register at {self.link}"
            )
            print(info) # noqa: T201


def display_banner() -> None:
    global _displayed_banner
    banner_info = DisplayInfo(title=title, info_text=info_text)

    if not _displayed_banner:
        banner_info.display_message()
        _displayed_banner = True
