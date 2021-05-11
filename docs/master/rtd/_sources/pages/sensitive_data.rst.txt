==============
Sensitive data
==============

When dealing with sensitive data, such as private health records, sharing a report that includes a sample would violate patient's privacy. The following shorthand groups together various options so that only aggregate information is provided in the report:

.. code-block:: python

  report = df.profile_report(sensitive=True)

Moreover, pandas-profiling does not send data to external services, making it suitable for private data.

Sample and duplicates
---------------------

The sample as well as duplicate rows are configurable. We can disable them using:

.. code-block:: python

  report = df.profile_report(duplicates=None, samples=None)

Alternatively, it's possible to bring your own custom sample.
The following snippet demonstrates how to generate the report with mock data.
Note that the "name" and "caption" keys are optional.

.. code-block:: python

  # Replace with the sample you'd like to present in the report
  sample_custom_data = pd.DataFrame()
  sample_description = "Disclaimer: the following sample consists of synthetic data following the format of the underlying dataset."

  report = df.profile_report(
      sample={
          "name": "Mock data sample",
          "data": sample_custom_data,
          "caption": sample_description,
      }
  )

.. warning::

   Be aware when using ``pandas.read_csv`` with sensitive data such as phone numbers.
   Pandas' type guessing will by default coerce phone numbers such as ``0612345678`` to numeric.
   This leads to information leakage through aggregates (min, max, quantiles).
   To prevent this from happening, keep the string representation.

   .. code-block:: python

        pd.read_csv("filename.csv", dtype={"phone": str})

   Note that the type detection is hard. That's the reason why we developed `visions <https://github.com/dylan-profiler/visions>`_, a type system to help developers solve these cases.
