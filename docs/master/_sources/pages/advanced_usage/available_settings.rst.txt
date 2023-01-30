==================
Available settings
==================

A set of options is available in order to customize the behaviour of ``ydata-profiling`` and the appearance of the generated report. The depth of customization allows the creation of behaviours highly targeted at the specific dataset being analysed. The available settings are listed below. To learn how to change them, check :doc:`changing_settings`.

General settings
----------------

Global report settings: 

.. csv-table::
   :file: ../tables/config_general.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1


Variable summary settings
-------------------------

Settings related with the information displayed for each variable. 

.. csv-table::
   :file: ../tables/config_variables.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1


.. code-block:: python
  :caption: Configuration example

  profile = df.profile_report(
      sort="ascending",
      vars={
          "num": {"low_categorical_threshold": 0},
          "cat": {
              "length": True,
              "characters": False,
              "words": False,
              "n_obs": 5,
          },
      },
  )

  profile.config.variables.descriptions = {
      "files": "Files in the filesystem",
      "datec": "Creation date",
      "datem": "Modification date",
  }

  profile.to_file("report.html")


Missing data overview plots
---------------------------

Settings related with the missing data section and the visualizations it can include. 

.. csv-table::
   :file: ../tables/config_missing.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1

.. code-block:: python
  :caption: Configuration example: disable heatmap for large datasets

  profile = df.profile_report(
      missing_diagrams={
          "heatmap": False,
      }
  )
  profile.to_file("report.html")

Correlations
------------

Settings regarding correlation metrics and thresholds.

.. csv-table::
   :file: ../tables/config_correlations.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1

For instance, to disable all correlation computations (may be relevant for large datasets):

.. code-block:: python

    profile = df.profile_report(
        title="Report without correlations",
        correlations={
            "auto": {"calculate": False},
            "pearson": {"calculate": False},
            "spearman": {"calculate": False},
            "kendall": {"calculate": False},
            "phi_k": {"calculate": False},
            "cramers": {"calculate": False},
        },
    )

    # or using a shorthand that is available for correlations
    profile = df.profile_report(
        title="Report without correlations",
        correlations=None,
    )


Interactions
------------

Settings related with the interactions section.  

.. csv-table::
   :file: ../tables/config_interactions.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1


Report's appearance
-------------------

Settings related with the appearance and style of the report.

.. csv-table::
   :file: ../tables/config_html.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1

