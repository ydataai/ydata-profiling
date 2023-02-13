==================
Dataset Comparison
==================

.. NOTE::
   **Dataframes compare support**
    - Profiling compare is supported from ydata-profiling version 3.5.0 onwards
    - Profiling compare is not *(yet!)* available for Spark Dataframes


``pandas-profiling`` can be used to compare multiple version of the same dataset.
This is useful when comparing data from multiple time periods, such as two years.
Another common scenario is to view the dataset profile for training, validation and test sets in machine learning.

The following syntax can be used to compare two datasets:

.. code-block:: python

    from pandas_profiling import ProfileReport

    train_df = pd.read_csv("train.csv")
    train_report = ProfileReport(train_df, title="Train")

    test_df = pd.read_csv("test.csv")
    test_report = ProfileReport(test_df, title="Test")

    comparison_report = train_report.compare(test_report)
    comparison_report.to_file("comparison.html")

The comparison report uses the ``title`` attribute out of ``Settings`` as a label throughout.
The colors are configured in ``settings.html.style.primary_colors``.
The numeric precision parameter ``settings.report.precision`` can be played with to obtain some additional space in reports.


In order to compare more than two reports, the following syntax can be used:

.. code-block:: python

    from pandas_profiling import ProfileReport, compare

    comparison_report = compare([train_report, validation_report, test_report])

    # Obtain merged statistics
    statistics = comparison_report.get_description()

    # Save report to file
    comparison_report.to_file("comparison.html")

Note that this functionality only ensures the support report comparison of two datasets.
It is possible to obtain the statistics - the report may have formatting issues.
One of the settings that can be changed is ``settings.report.precision``.
As a rule of thumb, the value 10 can be used for a single report and 8 for comparing two reports.
