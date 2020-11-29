"""Contains all templates used for generating the HTML profile report"""
import re
import shutil
from pathlib import Path

import jinja2

from pandas_profiling.config import config
from pandas_profiling.report.formatters import get_fmt_mapping

# Initializing Jinja
# from pandas_profiling.utils.paths import get_html_template_path

package_loader = jinja2.PackageLoader(
    "pandas_profiling", "report/presentation/flavours/html/templates"
)
jinja2_env = jinja2.Environment(
    lstrip_blocks=True, trim_blocks=True, loader=package_loader
)
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


def create_html_assets(output_file):
    theme = config["html"]["style"]["theme"].get(str)
    offline = config["html"]["use_local_assets"].get(bool)

    path = output_file.with_name(output_file.stem + "_assets")
    if path.is_dir():
        shutil.rmtree(path)

    path.joinpath("images").mkdir(parents=True, exist_ok=True)

    css = []
    js = []

    if offline:
        if theme != "None":
            if theme == "flatly":
                css.append("wrapper/assets/flatly.bootstrap.min.css")
            if theme == "united":
                css.append("wrapper/assets/united.bootstrap.min.css")
        else:
            css.append("wrapper/assets/bootstrap.min.css")
            css.append("wrapper/assets/bootstrap-theme.min.css")
        js.append("wrapper/assets/jquery-1.12.4.min.js")
        js.append("wrapper/assets/bootstrap.min.js")

    css.append("wrapper/assets/style.css")
    js.append("wrapper/assets/script.js")

    css_dir = path / "css"
    if not css_dir.exists():
        css_dir.mkdir()
        for css_file in css:
            (css_dir / Path(css_file).name).write_text(
                template(css_file).render(
                    primary_color=config["html"]["style"]["primary_color"].get(str),
                    nav=config["html"]["navbar_show"].get(bool),
                )
            )

    js_dir = path / "js"
    if not js_dir.exists():
        js_dir.mkdir()
        for js_file in js:
            (js_dir / Path(js_file).name).write_text(template(js_file).render())
