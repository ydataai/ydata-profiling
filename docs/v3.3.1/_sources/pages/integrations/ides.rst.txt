====
IDEs
====

The package can be directly consumed in some Integrated Development Environments, such as `PyCharm <https://www.jetbrains.com/pycharm/>`_. 

PyCharm
-------

1. Install ``pandas-profiling`` via :doc:`../getting_started/installation`
2. Locate your ``pandas-profiling`` executable.

  On macOS / Linux / BSD:

  .. code-block:: console

    $ which pandas_profiling
    (example) /usr/local/bin/pandas_profiling

  On Windows:

  .. code-block:: console

    $ where pandas_profiling
    (example) C:\ProgramData\Anaconda3\Scripts\pandas_profiling.exe

3. In PyCharm, go to *Settings* (or *Preferences* on macOS) > *Tools* > *External tools*
4. Click the **+** icon to add a new external tool
5. Insert the following values

  - Name: ``Pandas Profiling``

    - Program: *The location obtained in step 2*
    - Arguments: ``"$FilePath$" "$FileDir$/$FileNameWithoutAllExtensions$_report.html"``
    - Working Directory: ``$ProjectFileDir$``


.. image:: https://pandas-profiling.ydata.ai/docs/assets/pycharm-integration.png
  :alt: PyCharm Integration
  :width: 400
  :align: center

|

To use the PyCharm Integration, right click on any dataset file and *External Tools* > *Pandas Profiling*.