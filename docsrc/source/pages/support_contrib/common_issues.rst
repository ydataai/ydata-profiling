=============
Common issues
=============

TypeError: _plot_histogram() got an unexpected keyword argument 'title'
-----------------------------------------------------------------------

This error occurs when using outdated versions of the package.

Ensure that you are using the latest version, and when in a notebook, ensure that you've restarted the kernel when needed.
Also make sure that you install in the right Python environment (please use ``!{sys.executable} -m pip install -U pandas-profiling``!).
More information on installing Python packages directly from a notebook: `'Installing Python Packages from a Jupyter Notebook' <https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/>`_.

Related GitHub issues:
`[950] <https://github.com/ydataai/pandas-profiling/issues/950>`_, 
`[939] <https://github.com/ydataai/pandas-profiling/issues/939>`_, 
`[528] <https://github.com/ydataai/pandas-profiling/issues/528>`_, 
`[485] <https://github.com/ydataai/pandas-profiling/issues/485>`_, 
`[396] <https://github.com/ydataai/pandas-profiling/issues/396>`_


Conda installation defaults to v1.4.1
-------------------------------------

Some users experience that ``conda install -c conda-forge pandas-profiling`` defaults to 1.4.1.

If creating a new environment with a fresh installation does not resolve this issue, or the current environment must be kept, installing a specific version is one alternative to try: ``conda install -c conda-forge pandas-profiling=2.10.0``. 
If it fails with an ``UnsatisfiableError`` that suggests dependant packages are either missing or incompatible, then further intervention is required to resolve the *environment* issue. However, *conda* error messages in this regard may be too cryptic or insufficient to pinpoint the culprit, therefore you may have to resort to an alternate means of troubleshooting e.g using the `Mamba Package Manager <https://github.com/mamba-org/mamba.git>`_.
For an illustration of this approach see `this issue <https://github.com/pandas-profiling/pandas-profiling/issues/655>`_.

Related GitHub issues: `[22] <https://github.com/conda-forge/pandas-profiling-feedstock/issues/22>`_, `[448] <https://github.com/pandas-profiling/pandas-profiling/issues/448>`_, `[563] <https://github.com/pandas-profiling/pandas-profiling/issues/563>`_


Jupyter "IntSlider(value=0)"
----------------------------

When in a Jupyter environment, if only text such as ``IntSlider(value=0)`` or ``(children=(IntSlider(value=0, description='x', max=1), Output()), _dom_classes=('widget-interact',))`` is shown, then the Jupyter Widgets are not activated. The :doc:`../getting_started/installation` page contains instructions on how to resolve this problem.