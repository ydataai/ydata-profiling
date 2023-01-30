============
Installation
============

Using pip
---------

.. image:: https://pepy.tech/badge/pandas-profiling
  :alt: PyPi Total Downloads
  :target: https://pepy.tech/project/pandas-profiling

.. image:: https://pepy.tech/badge/pandas-profiling/month
  :alt: PyPi Monthly Downloads
  :target: https://pepy.tech/project/pandas-profiling/month

.. image:: https://badge.fury.io/py/pandas-profiling.svg
  :alt: PyPi Version
  :target: https://pypi.org/project/pandas-profiling/

You can install using the ``pip`` package manager by running:

.. code-block:: console

    pip install -U ydata-profiling

If you are in a notebook (locally, LambdaLabs, Google Colab or Kaggle), you can run:

.. code-block::

    import sys
    !{sys.executable} -m pip install -U ydata-profiling[notebook]
    !jupyter nbextension enable --py widgetsnbextension

You may have to restart the kernel or runtime for the package to work.

Using conda
-----------

.. image:: https://img.shields.io/conda/dn/conda-forge/pandas-profiling.svg
  :alt: Conda Total Downloads
  :target: https://anaconda.org/conda-forge/pandas-profiling

.. image:: https://img.shields.io/conda/vn/conda-forge/pandas-profiling.svg
  :alt: Conda Version
  :target: https://anaconda.org/conda-forge/pandas-profiling

A new conda environment containing the module can be created via: 

.. code-block:: console

    conda env create -n ydata-profiling
    conda activate ydata-profiling
    conda install -c conda-forge ydata-profiling

.. hint::

        Don't forget to specify the ``conda-forge`` channel. Omitting it **will not** lead to an error, as an outdated package lives on the ``main`` channel and will be installed. See :doc:`../support_contrib/common_issues` for details. 

Widgets in Jupyter Notebook/Lab
-------------------------------

For the Jupyter widgets extension (used for progress bars and the interactive widget-based report) to work, you might need to install and activate the corresponding extensions. 
This can be done via ``pip``: 

.. code-block::

  pip install pandas-profiling[notebook]
  jupyter nbextension enable --py widgetsnbextension

Or via ``conda``: 

.. code-block::

  conda install -c conda-forge ipywidgets

In most cases, this will also automatically configure Jupyter Notebook and Jupyter Lab (``>=3.0``). For older versions of both or in more complex
environment configurations, refer to `the official ipywidgets documentation <https://ipywidgets.readthedocs.io/en/stable/user_install.html>`_.

From source
-----------

Download the source code by cloning the repository or by clicking on `'Download ZIP' <https://github.com/ydataai/ydata-profiling/archive/master.zip>`_.
Install it by navigating to the uncompressed directory and running:

.. code-block:: console

    python setup.py install

This can also be done via the following one-liner: 

.. code-block:: console

    pip install https://github.com/ydataai/ydata-profiling/archive/master.zip

Extras
------

The package declares some "extras", sets of additional dependencies.

* ``[notebook]``: support for rendering the report in Jupyter notebook widgets.
* ``[unicode]``: support for more detailed Unicode analysis, at the expense of additional disk space.
* ``[pyspark]``: support for pyspark engine to run the profile on big datasets

Install these with e.g.

.. code-block:: console

    pip install -U ydata-profiling[notebook,unicode, pyspark]