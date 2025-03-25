import unittest

import pandas as pd

from ydata_profiling.utils.compat import optional_option_context, pandas_version_info


class TestCompatUtils(unittest.TestCase):
    def test_pandas_version_info_format(self):
        version_info = pandas_version_info()
        self.assertIsInstance(version_info, tuple)
        self.assertTrue(all(isinstance(i, int) for i in version_info))

        expected_prefix = tuple(
            int(x) for x in pd.__version__.split(".")[: len(version_info)]
        )
        self.assertEqual(version_info, expected_prefix)

    def test_optional_option_context_with_existing_option(self):
        option = "display.max_rows"
        original_value = pd.get_option(option)

        with optional_option_context(option, 123):
            self.assertEqual(pd.get_option(option), 123)

        self.assertEqual(pd.get_option(option), original_value)

    def test_optional_option_context_with_missing_option(self):
        class FakeOptionContext:
            def __init__(self, *args, **kwargs):
                raise pd.errors.OptionError("Simulated OptionError")

        original_option_context = pd.option_context
        pd.option_context = FakeOptionContext

        try:
            # Should not raise, even though the option is invalid
            with optional_option_context("non.existent.option", 456):
                pass
        finally:
            # Restore the original option_context
            pd.option_context = original_option_context


if __name__ == "__main__":
    unittest.main()
