===================================
Customizing the report's appearance
===================================

.. # TODO: Sentence explaining the dimensions of report customization

The HTML Report
---------------

.. csv-table::
   :file: ../tables/config_html.csv
   :widths: 30, 200, 200, 200
   :header-rows: 1

.. # TODO: link to settings

Customise plots
---------------
Plot rendering options
^^^^^^^^^^^^^^^^^^^^^^
A way how to pass arguments to the underlying matplotlib is to use the ``plot`` argument. It is possible to change the default format of images to png (default svg) using the key-pair ``image_format: "png"`` and also the resolution of the image using ``dpi: 800``.
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
Pie charts are used to plot the frequency of categories in categorical (or boolean) features.

By default, a feature is considered as categorical if it does not have more than 10 distinct values.
This threshold can be configured with the ``plot.pie.max_unique`` setting.

.. code-block:: python
    profile = ProfileReport(pd.DataFrame(["a", "b", "c"]))
    # Changing the *max_unique* threshold to 2 will make feature non-categorical
    profile.config.plot.pie.max_unique = 2

If the feature is not considered as categorical, the pie chart will not be displayed.

All pie charts can therefore be removed by setting: ``plot.pie.max_unique = 0``.

The pie chart colors can be configured to any `recognised matplotlib colour <https://matplotlib.org/stable/tutorials/colors/colors.html>`_
with the ``plot.pie.colors`` setting. 

.. code-block:: python
    profile = ProfileReport(pd.DataFrame([1, 2, 3]))
    profile.config.plot.pie.colors = ["gold", "b", "#FF796C"]

Customise correlation matrix
-----------------------------
It's possible to directly access the correlation matrix as well.
That is done with the ``plot`` argument and then with the ``correlation`` key.
It is possible to customise the palette, one can use the following list used in seaborn or create `their own custom matplotlib palette <https://matplotlib.org/stable/gallery/color/custom_cmap.html>`_.
Supported values are:

'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'


An example can be:

.. code-block:: python

  from pandas_profiling import ProfileReport

  profile = ProfileReport(
      df,
      title="Pandas Profiling Report",
      explorative=True,
      plot={"correlation": {"cmap": "RdBu_r", "bad": "#000000"}},
  )

Similarly, one can change the palette for *Missing values* using the ``missing`` argument, eg:

.. code-block:: python

  from pandas_profiling import ProfileReport

  profile = ProfileReport(
      df,
      title="Pandas Profiling Report",
      explorative=True,
      plot={"missing": {"cmap": "RdBu_r"}},
  )