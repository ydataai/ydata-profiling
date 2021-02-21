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

If you are in a notebook (locally, at LambdaLabs, on Google Colab or Kaggle), you can run:

.. code-block::

    import sys
    !{sys.executable} -m pip install -U pandas-profiling[notebook]
    !jupyter nbextension enable --py widgetsnbextension

You may have to restart the kernel or runtime.

Using conda
-----------

.. image:: https://img.shields.io/conda/dn/conda-forge/pandas-profiling.svg
  :alt: Conda Total Downloads
  :target: https://anaconda.org/conda-forge/pandas-profiling

.. image:: https://img.shields.io/conda/vn/conda-forge/pandas-profiling.svg
  :alt: Conda Version
  :target: https://anaconda.org/conda-forge/pandas-profiling

You can install using the conda package manager by running

.. code-block:: console

    conda env create -n pandas-profiling
    conda activate pandas-profiling
    conda install -c conda-forge pandas-profiling

This creates a new conda environment containing the module.

.. hint::

        Don't forget to specify the ``conda-forge`` channel. Omitting it won't result in an error, as an outdated package lives on the main channel. See `frequent issues <Support.rst#frequent-issues>`_

Jupyter notebook/lab
--------------------

For the Jupyter widgets extension to work, which is used for Progress Bars and the widget interface, you might need to activate the extensions. Installing with conda will enable the extension for you for Jupyter Notebooks (not lab).

For Jupyter notebooks:

.. code-block::

  jupyter nbextension enable --py widgetsnbextension

For Jupyter lab:

.. code-block::

  conda install -c conda-forge nodejs
  jupyter labextension install @jupyter-widgets/jupyterlab-manager


More information is available at the `ipywidgets documentation <https://ipywidgets.readthedocs.io/en/stable/user_install.html>`_.

From source
-----------

Download the source code by cloning the repository or by pressing `'Download ZIP' <https://github.com/pandas-profiling/pandas-profiling/archive/master.zip>`_ on this page.
Install by navigating to the proper directory and running

.. code-block:: console

    python setup.py install

This can also be done in one line:

.. code-block:: console

    pip install https://github.com/pandas-profiling/pandas-profiling/archive/master.zip
