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

You can install using the pip package manager by running

.. code-block:: console

    pip install -U pandas-profiling[notebook]
    jupyter nbextension enable --py widgetsnbextension

If you are in a notebook (locally, LambdaLabs, Google Colab or Kaggle), you can run:

.. code-block::

    import sys
    !{sys.executable} -m pip install -U pandas-profiling[notebook]
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

    conda env create -n pandas-profiling
    conda activate pandas-profiling
    conda install -c conda-forge pandas-profiling

.. hint::

        Don't forget to specify the ``conda-forge`` channel. Omitting it won't result in an error, as an outdated package lives on the ``main`` channel. See `frequent issues <Support.rst#frequent-issues>`_ for details. 

Widgets in Jupyter Notebook/Lab
-------------------------------

For the Jupyter widgets extension to work (used for progress bars and the interactive widget-based report), you might need to activate the corresponding extensions. 
This can be done via pip: 

.. code-block::

  pip install ipywidgets

Or via conda: 

.. code-block::

  conda install -c conda-forge ipywidgets

In most cases, this will also automatically configure both Jupyter Notebook and Jupyter Lab 3.0. For older versions of both or in more complex
environment configurations, refer to `the official ipywidgets documentation <https://ipywidgets.readthedocs.io/en/stable/user_install.html>`_.

From source
-----------

Download the source code by cloning the repository or by pressing `'Download ZIP' <https://github.com/ydataai/pandas-profiling/archive/master.zip>`_ on this page.
Install it by navigating to the uncompressed directory and running:

.. code-block:: console

    python setup.py install

This can also be done via the following one-liner: 

.. code-block:: console

    pip install https://github.com/ydataai/pandas-profiling/archive/master.zip