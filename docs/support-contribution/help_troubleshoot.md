# Help & Troubleshooting

## Troubleshooting

To start troubleshooting, we need to trace the issue to a bug in the
code or to something else (such as your local environment). The first
step is to create a new environment with a fresh installation (see
[Installation guide](../getting-started/installation.md) for
instructions). In many cases, the problem will be resolved by this step.

If the problem can be replicated in the new environment, then it likely
is a software bug. Before proceeding, check
`common_issues`{.interpreted-text role="doc"} to check whether it is a
previously identified common issue.

## Reporting a bug

To ensure the bug was not already reported by searching on Github under
[Issues](https://github.com/ydataai/ydata-profiling/issues). If you\'re
unable to find an open issue addressing the problem, [open a new
one](https://github.com/ydataai/ydata-profiling/issues/new/choose). If
possible, use the relevant bug report templates to create the issue.

You should provide the **minimal information to reproduce this bug**.
[This
guide](http://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports)
can help in crafting a minimal bug report. Please include:

-   The minimal code you are using to generate the report

-   Version information is essential in reproducing and resolving bugs.
    Include relevant environment details such as:

    > -   operating system (e.g. Windows, Linux, Mac)
    > -   Python version (e.g. `3.7`)
    > -   Interface: Jupyter notebook (or cloud services like Google
    >     Colab, Kaggle Kernels, etc), console or IDE (such as
    >     PyCharm,VS Code,etc)
    > -   package manager (e.g. `pip --version` or `conda info`)
    > -   packages (`pip freeze > packages.txt` or `conda list`). Please
    >     make sure this is contained in a collapsed section
    >     (instructions below)

-   a sample of the dataset (`df.sample()` or `df.head()`). If the
    dataset is confidential, for example when it contains
    company-sensitive information, provide us with a synthetic or open
    dataset that produces the same error. You can anonymize the column
    names if necessary.

-   a description of the dataset and its structure, for example by
    reporting the DataFrame\'s structure through the output of
    `df.info()`.

## Issue formatting

To craft helpful and easily readable issues, two formatting tricks are
recommended:

-   Code highlighting: wrap all code and error messages in fenced
    blocks, and in particular add the language identifier. Check the
    [Github docs on highlighting code
    blocks](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-and-highlighting-code-blocks)
    for details.
-   Collapsed sections: organize long error messages and requirement
    listings in collapsed sections. The [Github docs on collapsed
    sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
    provide detailed information.

## Using Stack Overflow

Users with a request for help on how to use `ydata-profiling` should
consider asking their question on Stack Overflow, under the dedicated
`ydata-profiling` tag:

[![Questions: Stackoverflow \"ydata-profiling\"](https://img.shields.io/badge/stackoverflow%20tag-ydata%20profiling-yellow)](https://stackoverflow.com/questions/tagged/ydata-profiling) or, 
[![Questions: Stackoverflow \"ydata-profiling\"](https://img.shields.io/badge/stackoverflow%20tag-pandas%20profiling-yellow)](https://stackoverflow.com/questions/tagged/pandas-profiling)

for questions about `ydata-profiling` older versions.

## :fontawesome-brands-discord: Discord community

[Join the Discord community](https://discord.com/invite/mw7xjJ7b7s) to
connect with both other users and developers that might be able to
answer your questions. The **#ydata-profiling** and **#need-help**
channels are recommended for questions and issues.
