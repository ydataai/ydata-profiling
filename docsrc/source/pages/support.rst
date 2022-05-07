=======
Support
=======

Troubleshooting
---------------

First, we need to know whether a problem is actually a bug in the code, or that it's caused by something else, such as your local environment. The first step is to create a new environment with a fresh installation. In many cases, the problem will be resolved by this step.

Frequent issues
~~~~~~~~~~~~~~~

TypeError: _plot_histogram() got an unexpected keyword argument 'title'
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This error occurs when using outdated versions of the package.

Ensure that you are using the latest version, and when in a notebook, ensure that you've restarted the kernel when needed!
Also make sure that you install in the right environment (please use ``!{sys.executable} -m pip install -U pandas-profiling``!).
Read more on this page: `'Installing Python Packages from a Jupyter Notebook' <https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/>`_.

Related issues:
`[950] <https://github.com/ydataai/pandas-profiling/issues/950>`_
`[528] <https://github.com/ydataai/pandas-profiling/issues/528>`_
`[485] <https://github.com/ydataai/pandas-profiling/issues/485>`_
`[396] <https://github.com/ydataai/pandas-profiling/issues/396>`_


Conda install defaults to v1.4.1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some users experience that ``conda install -c conda-forge pandas-profiling`` defaults to 1.4.1.

More details, `[22] <https://github.com/conda-forge/pandas-profiling-feedstock/issues/22>`_, `[448] <https://github.com/pandas-profiling/pandas-profiling/issues/448>`__ and `[563] <https://github.com/pandas-profiling/pandas-profiling/issues/563>`__.

If creating a new environment with a fresh installation does not resolve this issue, or you have good reason to persist with the current environment, then you could try installing a specific version e.g. ``conda install -c conda-forge pandas-profiling=2.10.0``. 
If it fails with an **UnsatisfiableError** that suggests dependant packages are either missing or incompatible, then further intervention is required to resolve the *environment* issue. However, *conda* error messages in this regard may be too cryptic or insufficient to pinpoint the culprit, therefore you may have to resort to an alternate means of troubleshooting e.g using the `Mamba Package Manager <https://github.com/mamba-org/mamba.git>`_.
For an illustration of this approach see `here <https://github.com/pandas-profiling/pandas-profiling/issues/655>`_.

Jupyter "IntSlider(value=0)"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
When in a Jupyter environment, you see some text, such as ``IntSlider(value=0)`` or interactive ``(children=(IntSlider(value=0, description='x', max=1), Output()), _dom_classes=('widget-interact',))``, then the Jupyter Widgets are not activated. The :doc:`installation` page contains instructions on how to resolve this problem.


Help on Stackoverflow
---------------------

Users with a request for help on how to use ``pandas-profiling`` should consider asking their question on stackoverflow.
There is a specific tag for ``pandas-profiling``:

.. image:: https://img.shields.io/badge/stackoverflow%20tag-pandas%20profiling-yellow
  :alt: Questions: Stackoverflow "pandas-profiling"
  :target: https://stackoverflow.com/questions/tagged/pandas-profiling

Slack community
---------------

`Join the Slack community <https://slack.ydata.ai>`_ and come into contact with other users and developers, that might be able to answer your questions.

Reporting a bug
---------------

Next, we want to ensure the bug was not already reported by searching on Github under `Issues <https://github.com/pandas-profiling/pandas-profiling/issues>`_. If you're unable to find an open issue addressing the problem, `open a new one <https://github.com/pandas-profiling/pandas-profiling/issues/new/choose>`_. If possible, use the relevant bug report templates to create the issue.

You should provide the minimal information to reproduce this bug. `This guide <http://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports>`_ can help crafting a minimal bug report. Please include:

- the minimal code you are using to generate the report

- Which environment you are using. Version information is essential in reproducing and resolving bugs. Please report relevant environment details such as:

        - operating system (e.g. Windows, Linux, Mac)
        - Python version (e.g. 3.7)
        - Jupyter notebook( or cloud services like Google Colab, Kaggle Kernels, etc), console or IDE (such as PyCharm,VS Code,etc)
        - package manager (e.g. ``pip --version`` or ``conda info``)
        - packages (``pip freeze > packages.txt`` or ``conda list``). Please make sure this is contained in a collapsed section (instructions below)

- a sample of the dataset (``df.sample()`` or ``df.head()``) Please share your dataframe. If the data is confidential, for example when it contains company-sensitive information, provide us with a synthetic or open dataset that produces the same error.
You can anonymize the column names if necessary.

- a description of the dataset (``df.info()``) You should provide the DataFrame structure, for example by reporting the output of ```df.info()``.

Issue formatting
----------------

- GitHub highlighting: wrap all code and error messages in fenced blocks, and in particular add the language identifier. Check the `Github docs on highlighting code blocks <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks>`_ for details.
- Organize long error messages and requirement listings in collapsed sections. The `Github docs on collapsed sections <https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections>`_ provide detailed information.


