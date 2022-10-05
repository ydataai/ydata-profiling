==================
Dataset Comparison
==================

*This feature was introduced in pandas-profiling 3.4.*

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

Note that generating reports for three or more datasets is not (yet) fully supported.
It is possible to obtain the statistics - the report may have formatting issues.
One of the settings that can be changed to improve the formatting is ``settings.report.precision``.
As a rule of thumb the value 10 can be used for a single report, 8 for comparing two reports and 5 for comparing three reports.

.. pull-quote::

    ⌛ Interested in uncovering more temporal patterns? Check out `popmon <https://github.com/ing-bank/popmon>`_.
