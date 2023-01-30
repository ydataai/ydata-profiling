========
Concepts
========

Data types
----------

Types, when going beyond the the logical data types such as integer, floats, etc,  are a powerful abstraction for effective data analysis, allowing analysis under higher level lenses. ``ydata-profiling`` is backed by a powerful type system developed specifically for data analysis: `visions <https://github.com/dylan-profiler/visions>`_. Currently, ``ydata-profiling`` recognizes the following types:

- Boolean
- Numerical
- Date (and Datetime)
- Categorical
- Time-series
- URL
- Path
- File
- Image

Appropriate typesets can both improve the overall expressiveness and reduce the complexity of the analysis/code. User customized summarizations and type definitions are fully supported, with PRs supporting new data types for specific use cases more than welcome. For reference, you can check the implementation of ``ydata-profiling``'s default typeset `here <https://github.com/ydataai/ydata-profiling/blob/develop/src/pandas_profiling/model/typeset.py>`_.

Data quality alerts
-------------------

.. figure::  ../../_static/warnings_section.png
  :alt: Data quality warnings
  :width: 100%
  :align: center

  Alerts section in the *NASA Meteorites* dataset's report. Some alerts include numerical indicators. 

The **Alerts** section of the report includes a comprehensive and automatic list of potential data quality issues. Although useful, the decision on whether an alert is in fact a data quality issue always requires domain validation. Some of the warnings refer to a specific column, others refer to inter-column relationships and others are dataset-wide. The table below lists all possible data quality alerts and their meanings.

.. csv-table::
   :file: ../tables/data_quality_alerts.csv
   :widths: 50, 350
   :header-rows: 1

Information on the default values and the specific parameters/thresholds used in the computation of these alerts, as well as settings to disable specific ones, can be consulted in :doc:`../advanced_usage/available_settings`. 
