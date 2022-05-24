===================================
Customizing the report's appearance
===================================

In some situations, a user might want to customize the appearance of the report to match personal preferences or a corporate brand. ``pandas-profiling`` offers two major customization dimensions: the **styling of the HTML report** and the **styling of the visualizations and plots** contained within. 

Customizing the report's theme
------------------------------

Several aspects of the report can be customized. The table below shows the available settings:

.. csv-table::
   :file: ../tables/config_html.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1

See :doc:`../advanced_usage/changing_settings` to see how to change and apply this settings.

Customizing the visualizations
------------------------------

Plot rendering options
^^^^^^^^^^^^^^^^^^^^^^
A way how to pass arguments to the underlying ``matplotlib`` visualization engine is to use the ``plot`` argument when computing the profile. It is possible to change the default format of images to png (default is SVG) using the key-pair ``image_format: "png"`` and also the resolution of the images using ``dpi: 800``.
An example would be:

.. code-block:: python

    profile = ProfileReport(
        planets,
        title="Pandas Profiling Report",
        explorative=True,
        plot={"dpi": 200, "image_format": "png"},
    )

Pie charts
^^^^^^^^^^

Pie charts are used to plot the frequency of categories in categorical (or boolean) features. By default, a feature is considered as categorical if it does not have more than 10 distinct values. This threshold can be configured with the ``plot.pie.max_unique`` setting.

.. code-block:: python
    profile = ProfileReport(pd.DataFrame(["a", "b", "c"]))
    # Changing the *max_unique* threshold to 2 will make feature non-categorical
    profile.config.plot.pie.max_unique = 2

If the feature is not considered as categorical, the pie chart will not be displayed. All pie charts can therefore be removed by setting: ``plot.pie.max_unique = 0``.

The pie chart's colors can be configured to any `recognised matplotlib colour <https://matplotlib.org/stable/tutorials/colors/colors.html>`_ with the ``plot.pie.colors`` setting. 

.. code-block:: python

    profile = ProfileReport(pd.DataFrame([1, 2, 3]))
    profile.config.plot.pie.colors = ["gold", "b", "#FF796C"]

Colour palettes
^^^^^^^^^^^^^^^

The palettes used in visualizations like correlation matrices and missing values overview can also be customized via the ``plot`` argument. To customize the palette used by the correlation matrix, use the ``correlation`` key:

.. code-block:: python

  from pandas_profiling import ProfileReport

  profile = ProfileReport(
      df,
      title="Pandas Profiling Report",
      explorative=True,
      plot={"correlation": {"cmap": "RdBu_r", "bad": "#000000"}},
  )

Similarly, the palette for *Missing values* can be changed using ``missing`` argument:

.. code-block:: python

  from pandas_profiling import ProfileReport

  profile = ProfileReport(
      df,
      title="Pandas Profiling Report",
      explorative=True,
      plot={"missing": {"cmap": "RdBu_r"}},
  )

``pandas-profiling`` accepts all ``cmap`` values (colormaps) accepted by ``matplotlib``. The list of available colourmaps can `be accessed here <https://matplotlib.org/stable/tutorials/colors/colormaps.html>`_. Alternatively, it is possible to create `custom palettes <https://matplotlib.org/stable/gallery/color/custom_cmap.html>`_.