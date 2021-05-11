========
Metadata
========

Dataset metadata
----------------
When sharing reports with coworkers or publishing online, you might want to include metadata of the dataset, such as author, copyright holder or a description. The supported properties are inspired by `https://schema.org/Dataset <https://schema.org/Dataset>`_. Currently supported are: "description", "creator", "author", "url", "copyright_year", "copyright_holder".

The following example generates a report with a "description", "copyright_holder" and "copyright_year", "creator" and "url".
You can find these properties in the "Overview" section under the "About" tab.

.. code-block:: python

    report = df.profile_report(
        title="Masked data",
        dataset={
            "description": "This profiling report was generated using a sample of 5% of the original dataset.",
            "copyright_holder": "StataCorp LLC",
            "copyright_year": "2020",
            "url": "http://www.stata-press.com/data/r15/auto2.dta",
        },
    )
    report.to_file(Path("stata_auto_report.html"))

Descriptions per variable
-------------------------
In addition to providing dataset details, users often would like to include column-specific descriptions when sharing reports with team members and stakeholders. This section provides two code examples how to do this in pandas-profiling.

.. code-block:: python
    :caption: Generate a report with descriptions per variable

    profile = df.profile_report(
        variables={
            "descriptions": {
                "files": "Files in the filesystem",
                "datec": "Creation date",
                "datem": "Modification date",
            }
        }
    )

    profile.to_file("report.html")


This alternative example demonstrates how you could load the definitions from a json file.
By default, the descriptions are presented in the overview tab and next to each variable.

.. code-block:: json
     :caption: dataset_column_definition.json

        {
            "column name 1": "column 1 definition",
            "column name 2": "column 2 definition"
        }

.. code-block:: python
        :caption: Generate a report with descriptions per variable from a definitions file

        import json
        import pandas as pd
        import pandas_profiling

        definition_file = "dataset_column_definition.json"

        # Read the variable descriptions
        with open(definition_file, "r") as f:
            definitions = json.load(f)

        # By default, the descriptions are presented in the overview tab and next to each variable
        report = df.profile_report(variable={"descriptions": definitions})

        # We can disable showing the descriptions next to each variable
        report = df.profile_report(
            variable={"descriptions": definitions}, show_variable_description=False
        )

        report.to_file('report.html')