=============
Big Datasets
=============

Pandas Profiling by default comprehensively summarizes the input dataset in a way that gives the most insights for data analysis.
For small datasets these computations can be performed in real-time.
For larger datasets, we have to decide upfront which calculations to make.
Whether a computation scales to big data not only depends on it's complexity, but also on fast implementations that are available.

You may try the options described in the following sections if calculation time is a bottleneck.

Minimal mode
------------

``pandas-profiling`` includes a minimal configuration file, with more expensive computations turned off by default.
This is a great starting point for larger datasets.

.. code-block:: python

  profile = ProfileReport(large_dataset, minimal=True)
  profile.to_file("output.html")


*(Minimal mode was introduced in ``pandas-profiling`` v2.4.0)*

The configuration file can be found here: `config_minimal.yaml <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_minimal.yaml>`_.

Sample
------

.. image:: ../_static/twitter_wisdom.png
  :target: https://twitter.com/ogrisel/status/951425284963733505

.. code-block:: python

  # Sample 10.000 rows
  sample = large_dataset.sample(10000)

  profile = ProfileReport(sample, minimal=True)
  profile.to_file("output.html")

The reader of the report might want to know that the profile is generated using a sample from the data.
An example of how to do this:

.. code-block:: python

  description = "Disclaimer: this profiling report was generated using a sample of 5% of the original dataset."
  sample = large_dataset.sample(frac=0.05)

  profile = sample.profile_report(description=description, minimal=True)
  profile.to_file("output.html")

Concurrency
-----------
``pandas-profiling`` is under active development.
One highly desired feature is to add a scalable backend such as `modin <https://github.com/modin-project/modin>`_, `spark <https://spark.apache.org/>`_ or `dask <https://dask.org/>`_.
Keep an eye on the `GitHub <https://github.com/pandas-profiling/pandas-profiling/issues>`_ page to follow the updates on concurrent implementation.