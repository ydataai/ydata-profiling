"""Contains all templates used for generating the HTML profile report"""
import jinja2
from jinja2 import Environment, PackageLoader

from pandas_profiling.view.formatters import (
    fmt_percent,
    fmt_bytesize,
    fmt_numeric,
    fmt_array,
    fmt,
)

# Initializing Jinja
package_loader = PackageLoader("pandas_profiling", "view/templates")
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=package_loader)
jinja2_env.filters["fmt_percent"] = fmt_percent
jinja2_env.filters["fmt_bytesize"] = fmt_bytesize
jinja2_env.filters["fmt_numeric"] = fmt_numeric
jinja2_env.filters["fmt_array"] = fmt_array
jinja2_env.filters["fmt"] = fmt


def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name.

    Args:
      template_name: The name of the template file (.html)

    Returns:
      The jinja2 environment.

    """
    return jinja2_env.get_template(template_name)
