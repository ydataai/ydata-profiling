=======
Support
=======

Troubleshooting
---------------

First, we need to know whether a problem is actually a bug in the code, or that it's caused by something else, such as your local environment. The first step is to create a new environment with a fresh installation. In many cases, the problem will be resolved by this step.

Frequent issues
~~~~~~~~~~~~~~~

- This thread discusses `conda installing older versions <https://github.com/conda-forge/pandas-profiling-feedstock/issues/22>`_ of the package.

- When in a Jupyter environment, you see some text, such as ``IntSlider(value=0)`` or interactive ``(children=(IntSlider(value=0, description='x', max=1), Output()), _dom_classes=('widget-interact',))``, then the Jupyter Widgets are not activated. The :doc:`installation` page contains instructions on how to resolve this problem.

Users with a request for help on how to use `pandas-profiling` should consider asking their question on stackoverflow. There is a specific tag for `pandas-profiling`:

.. image:: https://img.shields.io/badge/stackoverflow%20tag-pandas%20profiling-yellow
  :alt: Questions: Stackoverflow "pandas-profiling"
  :target: https://stackoverflow.com/questions/tagged/pandas-profiling


Reporting a bug
---------------

Next, we want to ensure the bug was not already reported by searching on Github under `Issues <https://github.com/pandas-profiling/pandas-profiling/issues>`_. If you're unable to find an open issue addressing the problem, `open a new one <https://github.com/pandas-profiling/pandas-profiling/issues/new/choose>`_. If possible, use the relevant bug report templates to create the issue.

You should provide the minimal information to reproduce this bug. `This guide <http://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports>`_ can help crafting a minimal bug report. Please include:

- the minimal code you are using to generate the report

- which environment you are using:

        - operating system (e.g. Windows, Linux, Mac)
        - Python version (e.g. 3.7)
        - jupyter notebook, console or IDE such as PyCharm
        - Package manager (e.g. pip, conda conda info)
        - packages (pip freeze > packages.txt or conda list)

- a sample or description of the dataset ``df.head(), df.info()``
