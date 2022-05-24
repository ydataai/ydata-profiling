==========
Quickstart
==========

Start by loading your pandas ``DataFrame`` as you normally would, e.g. by using:

.. code-block:: python

        import numpy as np
        import pandas as pd
        from pandas_profiling import ProfileReport

        df = pd.DataFrame(np.random.rand(100, 5), columns=["a", "b", "c", "d", "e"])

To generate the standard profiling report, merely run:

.. code-block:: python

        profile = ProfileReport(df, title="Pandas Profiling Report")


Using inside Jupyter Notebooks
------------------------------

There are two interfaces to consume the report inside a Jupyter notebook (see animations below): through widgets and through an embedded HTML report.

.. image:: ../../_static/widgets.gif

This is achieved by simply displaying the report as a set of widgets. In a Jupyter Notebook, run:

.. code-block:: python

  profile.to_widgets()

The HTML report can be directly embedded in a cell in a similar fashion:

.. code-block:: python

  profile.to_notebook_iframe()

.. image:: ../../_static/iframe.gif


Exporting the report to a file
------------------------------
To generate a HTML report file, save the ``ProfileReport`` to an object and use the ``to_file()`` function:

.. code-block:: python

        profile.to_file("your_report.html")

Alternatively, the report's data can be obtained as a JSON file:

.. code-block:: python

        # As a JSON string
        json_data = profile.to_json()

        # As a file
        profile.to_file("your_report.json")


Command line usage
------------------
For standard formatted CSV files (which can be read directly by pandas without additional settings), the ``pandas_profiling`` executable can be used in the command line:

.. code-block:: bash

        pandas_profiling -h

The snippet above displays information about options and arguments.


Deeper profiling
----------------

The contents, behaviour and appearance of the report are easily customizable. The example code below loads the `explorative configuration file <https://github.com/ydataai/pandas-profiling/blob/master/src/pandas_profiling/config_explorative.yaml>`_, 
which includes many features for text analysis (length distribution, word distribution and character/unicode information), files (file size, creation time) and images (dimensions, EXIF information). 
These exact settings used in this explorative configuration file can be compared with the `default configuration file <https://github.com/ydataai/pandas-profiling/blob/master/src/pandas_profiling/config_default.yaml>`_.

.. code-block:: python

        profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)


Learn more about configuring ``pandas-profiling`` on the :doc:`../advanced_usage/available_settings` page. 