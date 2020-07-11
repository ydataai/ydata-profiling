========
Metadata
========

When sharing reports with coworkers or publishing online, you might want to include metadata of the dataset, such as author, copyright holder or a description. The supported properties are inspired by `https://schema.org/Dataset <https://schema.org/Dataset>`_. Currently supported are: "description", "creator", "author", "url", "copyright_year", "copyright_holder".

The following example generates a report with a "description", "copyright_holder" and "copyright_year", "creator" and "url".
You can find these properties in the "Overview" section under the "About" tab.

.. code-block:: python

    report = df.profile_report(
        title="Masked data",
        dataset=dict(
            description="This profiling report was generated using a sample of 5% of the original dataset.",
            copyright_holder="StataCorp LLC",
            copyright_year="2020",
            url="http://www.stata-press.com/data/r15/auto2.dta",
        ),
    )
    report.to_file(Path("stata_auto_report.html"))
