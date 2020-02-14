"""Contains all templates used for generating the HTML profile report"""
import re

import jinja2
from jinja2 import Environment, PackageLoader

from pandas_profiling.report.formatters import get_fmt_mapping

# Initializing Jinja
package_loader = PackageLoader(
    "pandas_profiling", "report/presentation/flavours/html/templates"
)
jinja2_env = Environment(lstrip_blocks=True, trim_blocks=True, loader=package_loader)
fmt_mapping = get_fmt_mapping()
for key, value in fmt_mapping.items():
    jinja2_env.filters[key] = value

jinja2_env.filters["fmt_badge"] = lambda x: re.sub(
    r"\((\d+)\)", r'<span class="badge">\1</span>', x
)
jinja2_env.filters["dynamic_filter"] = lambda x, v: fmt_mapping[v](x)


def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name.

    Args:
      template_name: The name of the template file (.html)

    Returns:
      The jinja2 environment.

    """
    return jinja2_env.get_template(template_name)
