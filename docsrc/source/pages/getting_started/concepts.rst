========
Concepts
========

Data types
----------

Types, when going beyond the the logical data types such as integer, floats, etc,  are a powerful abstraction for effective data analysis, allowing analysis under higher level lenses. ``pandas-profiling`` is backed by a powerful type system developed specifically for data analysis: `visions <https://github.com/dylan-profiler/visions>`_. Currently, ``pandas-profiling`` recognizes the following types: 

- Boolean
- Numerical
- Date (and Datetime)
- Categorical
- URL
- Path
- File
- Image

Appropriate typesets can both improve the overall expressiveness and reduce the complexity of the analysis/code. User customized summarizations and type definitions are fully supported, with PRs supporting new data types for specific use cases more than welcome. For reference, you can check the implementation of ``pandas-profiling``'s default typeset `here <https://github.com/ydataai/pandas-profiling/blob/develop/src/pandas_profiling/model/typeset.py>`_. 

Data quality warnings
---------------------

.. figure::  ../../_static/warnings_section.png
  :alt: Data quality warnings
  :width: 100%
  :align: center

.. TODO: Add legend


The **Warnings** section of the report includes a comprehensive and automatic list of potential data quality issues. Some are evaluated per column, others refer to inter-column relationships while others are dataset-wide. The table below lists all possible data quality warnings and their meaning. 

.. csv-table::
   :file: ../tables/data_quality_warnings.csv
   :widths: 30, 200, 200
   :header-rows: 1


Information on the default values and the specific parameters/thresholds used in the computation of these warnings can be consulted in :doc:`../advanced_usage/available_settings`. 
