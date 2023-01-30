"""Utility functions that come in handy when working with Jupyter notebooks"""


def full_width() -> None:
    """Resize the notebook to use it's full width"""
    from IPython.core.display import HTML, display

    display(HTML("<style>.container { width:100% !important; }</style>"))
