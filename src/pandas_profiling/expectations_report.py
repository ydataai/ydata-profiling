from pandas_profiling.model import expectation_algorithms
from pandas_profiling.model.handler import Handler
from pandas_profiling.model.typeset import (
    URL,
    Boolean,
    Categorical,
    DateTime,
    File,
    Image,
    Numeric,
    Path,
    ProfilingTypeSet,
    Unsupported,
)
from pandas_profiling.utils.dataframe import slugify


# Default handler
class ExpectationHandler(Handler):
    def __init__(self, typeset, *args, **kwargs):
        mapping = {
            Unsupported: [expectation_algorithms.generic_expectations],
            Categorical: [expectation_algorithms.categorical_expectations],
            Numeric: [expectation_algorithms.numeric_expectations],
            URL: [expectation_algorithms.url_expectations],
            File: [expectation_algorithms.file_expectations],
            Path: [expectation_algorithms.path_expectations],
            Boolean: [expectation_algorithms.boolean_expectations],
            DateTime: [expectation_algorithms.datetime_expectations],
            Image: [expectation_algorithms.image_expectations],
        }
        super().__init__(mapping, typeset, *args, **kwargs)


class ExpectationsReport:
    def to_expectations_suite(self, suite_name=None, handler=None):
        try:
            import great_expectations as ge
        except ImportError:
            raise ImportError(
                "Please install great expectations before using the expectation functionality"
            )

        # Use report title if suite is empty
        if suite_name is None:
            suite_name = slugify(self.title)

        # Use the default handler if none
        if handler is None:
            handler = ExpectationHandler(ProfilingTypeSet())

        # Obtain the ge context and create the expectation suite
        context = ge.data_context.DataContext()
        suite = context.create_expectation_suite(suite_name, overwrite_existing=True)
        context.save_expectation_suite(suite)

        # Instantiate an in-memory pandas dataset
        batch = ge.dataset.PandasDataset(self.df, expectation_suite=suite)

        # Obtain the profiling summary
        summary = self.get_description()

        # Dispatch to expectations per semantic variable type
        for name, variable_summary in summary["variables"].items():
            handler.handle(variable_summary["type"], name, variable_summary, batch)

        return batch

    def to_expectations(self, suite_name=None, handler=None, build_data_docs=True):
        try:
            import great_expectations as ge
        except ImportError:
            raise ImportError(
                "Please install great expectations before using the expectation functionality"
            )

        context = ge.data_context.DataContext()

        batch = self.to_expectations_suite(suite_name, handler)

        results = context.run_validation_operator(
            "action_list_operator", assets_to_validate=[batch]
        )
        validation_result_identifier = results.list_validation_result_identifiers()[0]

        # Write expectations and open data docs
        context.save_expectation_suite(batch.get_expectation_suite())

        if build_data_docs:
            context.build_data_docs()
            context.open_data_docs(validation_result_identifier)
