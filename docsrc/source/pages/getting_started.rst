===============
Getting started
===============

Getting started
Start by loading in your pandas DataFrame, e.g. by using

.. code-block:: python

        import numpy as np
        import pandas as pd
        from pandas_profiling import ProfileReport

        df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])

To generate the report, run:

.. code-block:: python

        profile = ProfileReport(df, title="Pandas Profiling Report")


Explore deeper
--------------

You can configure the profile report in any way you like. The example code below loads the `explorative configuration file <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_explorative.yaml>`_, that includes many features for text (length distribution, word distribution and character/unicode information), files (file size, creation time) and images (dimensions, exif information). If you are interested what exact settings were used, you can compare with the `default configuration file <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/config_default.yaml>`_.

.. code-block:: python

        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)


Learn more about configuring ``pandas-profiling`` on the :doc:`advanced_usage` page.

Jupyter notebook
----------------

We recommend generating reports interactively by using the Jupyter notebook. There are two interfaces (see animations below): through widgets and through a HTML report.

.. image:: ../_static/widgets.gif

This is achieved by simply displaying the report. In the Jupyter Notebook, run:

.. code-block:: python

  profile.to_widgets()

The HTML report can be included in a Jupyter notebook:

.. image:: ../_static/iframe.gif

Run the following code:

.. code-block:: python

  profile.to_notebook_iframe()


Saving the report
-----------------
If you want to generate a HTML report file, save the ``ProfileReport`` to an object and use the ``to_file()`` function:

.. code-block:: python

        profile.to_file("your_report.html")

Alternatively, you can obtain the data as json:

.. code-block:: python

        # As a string
        json_data = profile.to_json()

        # As a file
        profile.to_file("your_report.json")



Command line usage
------------------
For standard formatted CSV files that can be read immediately by pandas, you can use the pandas_profiling executable. Run

.. code-block:: bash

        pandas_profiling -h

for information about options and arguments.