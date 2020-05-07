==============
Sensitive data
==============

When dealing with sensitive data, such as private health records, sharing a report that includes a sample would violate patient's privacy. The sample can be disabled with the following settings:

.. code-block:: python

  report = df.profile_report(samples={"head": 0, "tail": 0})

Moreover, `pandas-profiling` does not send data to external services, making it suitable for private data.