"""Code for generating plots"""
from pandas_profiling.utils.packages import is_installed

if is_installed("altair"):
    import pandas_profiling.visualisation.altair_
if is_installed("matplotlib"):
    import pandas_profiling.visualisation.matplotlib_
import pandas_profiling.visualisation.plot
