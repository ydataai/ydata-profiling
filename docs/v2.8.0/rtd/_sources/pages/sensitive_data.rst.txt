==============
Sensitive data
==============

When dealing with sensitive data, such as private health records, sharing a report that includes a sample would violate patient's privacy. The sample as well as duplicate rows are configurable. We can disable them using:

.. code-block:: python

  report = df.profile_report(duplicates=None, samples=None)

Moreover, `pandas-profiling` does not send data to external services, making it suitable for private data.