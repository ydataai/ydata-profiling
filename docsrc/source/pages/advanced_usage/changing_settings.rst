=================
Changing settings
=================

Using a custom configuration file
---------------------------------

To set the configuration of pandas-profiling using a custom file, you can start one of the sample configuration files below.
Then, change the configuration to your liking.

.. code-block:: python

  from pandas_profiling import ProfileReport

  profile = ProfileReport(df, config_file="your_config.yml")
  profile.to_file("report.html")

Sample configuration files
--------------------------
A great way to get an overview of the possible configuration is to look through sample configuration files.
The repository contains the following files:

- `default configuration file <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_default.yaml>`_ (default),
- `minimal configuration file <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_minimal.yaml>`_ (minimal computation, optimized for performance)

Configuration shorthands
------------------------

It's possible to disable certain groups of features through configuration shorthands.

.. code-block:: python

    # Disable samples, correlations, missing diagrams and duplicates at once
    r = ProfileReport(
        samples=None,
        correlations=None,
        missing_diagrams=None,
        duplicates=None,
        interactions=None,
    )

Read config from environment
----------------------------
Any profile report config setting can also be read in from environment variables.

For example:

.. code-block:: python

    from pandas_profiling import ProfileReport

    profile = ProfileReport(df, title="My Custom Pandas Profiling Report")

is equivalent to setting the title as an environment variable

.. code-block:: console

    export PROFILE_TITLE="My Custom Pandas Profiling Report"

and running

.. code-block:: python

    from pandas_profiling import ProfileReport

    profile = ProfileReport(df)
