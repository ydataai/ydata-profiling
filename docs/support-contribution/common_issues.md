# Common issues

## TypeError: \_plot_histogram() got an unexpected keyword argument \'title\'

This error occurs when using outdated versions of the package.

Ensure that you are using the latest version, and when in a notebook,
ensure that you\'ve restarted the kernel when needed. Also make sure
that you install in the right Python environment (please use
`!{sys.executable} -m pip install -U ydata-profiling`!). More
information on installing Python packages directly from a notebook:
[\'Installing Python Packages from a Jupyter
Notebook\'](https://jakevdp.github.io/blog/2017/12/05/installing-python-packages-from-jupyter/).

Related GitHub issues:

-   [\[950\]](https://github.com/ydataai/ydata-profiling/issues/950)
-   [\[939\]](https://github.com/ydataai/ydata-profiling/issues/939)
-   [\[528\]](https://github.com/ydataai/ydata-profiling/issues/528)
-   [\[485\]](https://github.com/ydataai/ydata-profiling/issues/485)
-   [\[396\]](https://github.com/ydataai/ydata-profiling/issues/396)

## Jupyter \"IntSlider(value=0)\"

When in a Jupyter environment, if only text such as `IntSlider(value=0)`
or
`(children=(IntSlider(value=0, description='x', max=1), Output()), _dom_classes=('widget-interact',))`
is shown, then the Jupyter Widgets are not activated. The
`../getting_started/installation`{.interpreted-text role="doc"} page
contains instructions on how to resolve this problem.

## MemoryError: Unable to allocate\... when profiling datasets with very large values

A memory error that comes up when profiling datasets with large outliers
(even if the dataset itself is small), which is due to an underlying bug
in `numpy`, used to build a histogram. Although some [workarounds are
suggested on numpy\'s
GitHub](https://github.com/numpy/numpy/issues/10297), the bug is not yet
fixed. One workaround is to filter out large outliers prior to report
computation.

Related StackOverflow questions:
-   [MemoryError when using ydata_profiling
    profile_report](https://stackoverflow.com/questions/67342168/memoryerror-when-using-pandas-profiling-profile-report)
