====================================
Integration with Great Expectations
====================================

`Great Expectations <https://www.greatexpectations.io>`_ is a Python-based open-source library for validating, documenting, and profiling your data. It helps you to maintain data quality and improve communication about data between teams. With Great Expectations, you can assert what you expect from the data you load and transform, and catch data issues quickly – Expectations are basically *unit tests for your data*. Pandas Profiling features a method to create a suite of Expectations based on the results of your ProfileReport!


About Great Expectations
-------------------------

*Expectations* are assertions about your data. In Great Expectations, those assertions are expressed in a declarative language in the form of simple, human-readable Python methods. For example, in  order to assert that you want values in a column ``passenger_count`` in your dataset to be integers between 1 and 6, you can say:

    ``expect_column_values_to_be_between(column="passenger_count", min_value=1, max_value=6)``

Great Expectations then uses this statement to validate whether the column ``passenger_count`` in a given table is indeed between 1 and 6, and returns a success or failure result. The library currently provides `several dozen highly expressive built-in Expectations <https://docs.greatexpectations.io/en/latest/reference/glossary_of_expectations.html>`_, and allows you to write custom Expectations.

Great Expectations renders Expectations to clean, human-readable documentation called *Data Docs*. These HTML docs contain both your Expectation Suites as well as your data validation results each time validation is run – think of it as a continuously updated data quality report.

For more information about Great Expectations, check out the `Great Expectations documentation <https://docs.greatexpectations.io/en/latest/>`_ and join the `Great Expectations Slack channel <https://www.greatexpectations.io/slack>` for help.


Creating Expectation Suites with Pandas Profiling
--------------------------------------------------

An *Expectation Suite* is simply a set of Expectations. You can create Expectation Suites by writing out individual statements, such as the one above, or by automatically generating them based on profiler results.

Pandas Profiling provides a simple ``to_expectation_suite()`` method that returns a Great Expectations ``ExpectationSuite`` object which contains a set of Expectations.

**Pre-requisites**: In order to run the ``to_expectation_suite()`` method, you will need to install Great Expectations:
`pip install great_expectations`

If you would like to use the additional features such as saving the Suite and building Data Docs, you will also need to configure a Great Expectations Data Context by running ``great_expectations init`` while in your project directory.

.. code-block:: python

    import pandas as pd
    from pandas_profiling import ProfileReport

    df = pd.read_csv("titanic.csv")

    profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

    # Obtain an Expectation Suite with a set of default Expectations
    # By default, this also profiles the dataset, saves the suite, runs validation, and builds Data Docs
    suite = profile.to_expectation_suite()


This assumes that the ``great_expectations`` Data Context directory is in the *same path* where you run the script. In order to specify the location of your Data Context, pass it in as an argument:

.. code-block:: python

    import great_expectations as ge

    data_context = ge.data_context.DataContext(context_root_dir="/Users/panda/code/my_ge_project/")
    suite = profile.to_expectation_suite(data_context=data_context)


You can also configure each feature individually in the function call:

.. code-block:: python

    suite = profile.to_expectation_suite(
        suite_name="titanic_expectations",
        data_context=data_context,
        save_suite=False,
        run_validation=False,
        build_data_docs=False,
        handler=handler
    )

See `the Great Expectations Examples <https://pandas-profiling.github.io/pandas-profiling/examples/master/features/great_expectations_example.html>`_ for complete examples.


Included Expectation types
--------------------------

The ``to_expectation_suite`` method returns a default set of Expectations if Pandas Profiling determines that the assertion holds true for the profiled dataset.
The Expectation types depend on the datatype of a column:

**All columns**

* ``expect_column_values_to_not_be_null``
* ``expect_column_values_to_be_unique``

**Numeric columns**

* ``expect_column_values_to_be_in_type_list``
* ``expect_column_values_to_be_increasing``
* ``expect_column_values_to_be_decreasing``
* ``expect_column_values_to_be_between``

**Categorical columns**

* ``expect_column_values_to_be_in_set``

**Datetime columns**

* ``expect_column_values_to_be_between``

**Filename columns**

* ``expect_file_to_exist``


The default logic is straight forward and can be found here in `expectation_algorithms.py <https://github.com/pandas-profiling/pandas-profiling/blob/master/src/pandas_profiling/model/expectation_algorithms.py>`_.

Rolling your own Expectation Generation Logic
---------------------------------------------

If you would like to profile datasets at scale, your use case might require changing the default expectations logic.
The ``to_expectation_suite`` takes the ``handler`` parameter, which allows you to take full control of the generation process.
Generating expectations takes place in two steps:

- mapping the detected type of each column to a generator function (that receives the columns' summary statistics);
- generating expectations based on the summary (e.g. ``expect_column_values_to_not_be_null`` if ``summary["n_missing"] == 0``)

Adding an expectation to columns with constant length can be achieved for instance using this code:

.. code-block:: python

    def fixed_length(name, summary, batch, *args):
        """Add a length expectation to columns with constant length values"""
        if summary["min_length"] == summary["max_length"]:
            batch.expect_column_value_lengths_to_equal(summary["min_length"])
        return name, summary, batch


    class MyExpectationHandler(Handler):
        def __init__(self, typeset, *args, **kwargs):
            mapping = {
                Unsupported: [expectation_algorithms.generic_expectations],
                Categorical: [expectation_algorithms.categorical_expectations, fixed_length],
                Boolean: [expectation_algorithms.categorical_expectations],
                Numeric: [expectation_algorithms.numeric_expectations],
                URL: [expectation_algorithms.url_expectations],
                File: [expectation_algorithms.file_expectations],
                Path: [expectation_algorithms.path_expectations],
                DateTime: [expectation_algorithms.datetime_expectations],
                Image: [expectation_algorithms.image_expectations],
            }
            super().__init__(mapping, typeset, *args, **kwargs)

    # (initiate report)

    suite = report.to_expectation_suite(
        handler=MyExpectationHandler(report.typeset)
    )

You can automate even more by extending the typeset (by default the ``ProfilingTypeSet``) with semantic data types specific to your company or use case (for instance disease classification in healthcare or currency and IBAN in finance).
For that, you can find details in the `visions <https://github.com/dylan-profiler/visions>`_ documentation.
