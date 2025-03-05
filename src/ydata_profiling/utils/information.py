"""
    References and information regarding ydata-profiling and ydata-sdk
"""
import sys
from IPython.display import HTML, display

_displayed_banner = False

link='https://ydata.ai/register'
title='Upgrade to ydata-sdk'
info_text='Improve your data and profiling with ydata-sdk, featuring data quality scoring, redundancy detection, outlier identification, text validation, and synthetic data generation.'

def in_jupyter_notebook():
    """Check if the code is running inside a Jupyter Notebook"""
    try:
        from IPython import get_ipython
        return get_ipython() is not None
    except ImportError:
        return False

def display_banner():
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
        print(f"\033[1;34m{title}\033[0m")  # Bold blue title in terminal
        print(info_text)
        print(f"Register at {link}")
        _displayed_banner = True