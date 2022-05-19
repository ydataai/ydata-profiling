========================
Help & Troubleshooting
========================

Troubleshooting
---------------

First, we need to know whether a problem is actually a bug in the code, or that it's caused by something else, such as your local environment. The first step is to create a new environment with a fresh installation. In many cases, the problem will be resolved by this step.

.. #TODO: link to common issues


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


