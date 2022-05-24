========================================
Caching results throughout multiple runs
========================================

The ``ProfileReport`` object caches intermediary results for improved performance, which exported HTML and JSON files will reuse. 

If you modify the configuration in-between runs, either a new ``ProfileReport`` object should be created or relevant cached values should be invalidated through ``report.invalidate_cache()``. The specific set of caches to reset can be passed as an argument to the ``ìnvalidate_cache()`` method: 

- *rendering* to invalidate previously rendered reports (HTML, JSON or widgets)
- *report* to remove the caching of the report's structure
- *None* (default) to invalidate all caches