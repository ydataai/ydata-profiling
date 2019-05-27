"""Main module of pandas-profiling.

.. include:: ../README.md
"""
from pathlib import Path

from pandas_profiling.config import config
from pandas_profiling.controller import pandas_decorator
import pandas_profiling.view.templates as templates
from pandas_profiling.model.describe import describe as describe_df
from pandas_profiling.utils.paths import get_config_default
from pandas_profiling.view.report import to_html


class ProfileReport(object):
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.
    
    Used has is it will output its content as an HTML report in a Jupyter notebook.
    """

    html: str = ""
    """the HTML representation of the report, without the wrapper (containing `<head>` etc.)"""

    def __init__(self, df, **kwargs):
        config.set_kwargs(kwargs)

        # Get dataset statistics
        description_set = describe_df(df)

        # Get sample
        sample = {}
        if config["samples"]["head"].get(int) > 0:
            sample["head"] = df.head(config["samples"]["head"].get(int))
        if config["samples"]["tail"].get(int) > 0:
            sample["tail"] = df.tail(config["samples"]["tail"].get(int))

        # Render HTML
        self.html = to_html(sample, description_set)
        self.minify_html = config["minify_html"].get(bool)
        self.title = config["title"].get(str)
        self.description_set = description_set
        self.sample = sample

    def get_description(self) -> dict:
        """Return the description (a raw statistical summary) of the dataset.
        
        Returns:
            Dict containing a description for each variable in the DataFrame.
        """
        return self.description_set

    def get_rejected_variables(self, threshold: float = 0.9) -> list:
        """Return a list of variable names being rejected for high 
        correlation with one of remaining variables.
        
        Args:
            threshold: correlation value which is above the threshold are rejected (Default value = 0.9)

        Returns:
            A list of rejected variables.
        """
        variable_profile = self.description_set["variables"]
        result = []
        for col, values in variable_profile.items():
            if "correlation" in values:
                if values["correlation"] > threshold:
                    result.append(col)
        return result

    def to_file(self, output_file: Path or str) -> None:
        """Write the report to a file.
        
        By default a name is generated.

        Args:
            output_file: The name or the path of the file to generate including the extension (.html).        
        """
        # outputfile = Path('profile_' + str(hash(self)) + ".html")
        if type(output_file) == str:
            output_file = Path(output_file)

        with output_file.open("w", encoding="utf8") as f:
            wrapped_html = templates.template("wrapper.html").render(
                content=self.html,
                title=self.title,
                correlation=len(self.description_set["correlations"]) > 0,
                missing=len(self.description_set["missing"]) > 0,
                sample=len(self.sample) > 0,
            )
            if self.minify_html:
                from htmlmin.main import minify

                wrapped_html = minify(
                    wrapped_html, remove_all_empty_space=True, remove_comments=True
                )
            f.write(wrapped_html)

    def to_html(self) -> str:
        """Generate and return complete template as lengthy string
            for using with frameworks.

        Returns:
            Profiling report html including wrapper.
        
        """
        return templates.template("wrapper.html").render(
            content=self.html,
            title=self.title,
            correlation=len(self.description_set["correlations"]) > 0,
            missing=len(self.description_set["missing"]) > 0,
            sample=len(self.sample) > 0,
        )

    def _repr_html_(self) -> str:
        """Used to output the HTML representation to a Jupyter notebook"""
        return self.html

    def get_style(self):
        """
        In Notebooks, we do not need the wrapper HTML, but we need the style.

        Returns:
            style for the profiling report, wrapped in `<style>` tag.
        """
        return templates.template("style.html").render()
