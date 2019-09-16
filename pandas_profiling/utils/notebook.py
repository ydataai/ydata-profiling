"""Utility functions that come in handy when working with Jupyter notebooks"""


def full_width():
    """Resize the notebook to use it's full width"""
    from IPython.core.display import display, HTML

    display(HTML("<style>.container { width:100% !important; }</style>"))


def in_ipynb() -> bool:
    """ Detects whether the environment is running by a jupyter notebook """
    try:
        __IPYTHON__
    except NameError:
        return False
    else:
        return True
