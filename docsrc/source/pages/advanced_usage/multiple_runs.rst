=============
Multiple runs
=============

Multiple runs
-------------
The ProfileReport caches intermediary results for improved performance.
For rendering both the HTMl report write the statistics as a JSON file will reuse the same computations.
If you modify the configuration in between runs, you should either create a new ``ProfileReport`` object or invalidate the relevant cached values.
If the config for only the HTML report is changed (for instance you would like to tune the theme), then you only need to reset the cached HTML report.
You can use the ``report.invalidate_cache()`` method for this.
Passing the values "rendering" only resets previously rendered reports (HTML, JSON or widgets).
Alternatively "report" also resets the report structure.