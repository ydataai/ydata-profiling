# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import date

sys.path.insert(0, os.path.join("..", "..", "src"))
sys.path.insert(0, os.path.join("..", "..", "src", "ydata_profiling"))


# -- Project information -----------------------------------------------------

project = "ydata-profiling"
year = date.today().year
copyright = f"{year}, YData Labs Inc"
author = "YData Labs Inc"

# The full version, including alpha/beta/rc tags


def _GetApiWrapperVersion():
    import pkg_resources

    return pkg_resources.get_distribution("ydata-profiling").version


release = _GetApiWrapperVersion()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.viewcode",
    "sphinxcontrib.autodoc_pydantic",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build"]

master_doc = "index"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = "sphinx_rtd_theme"
html_theme_options = {"style_nav_header_background": "#e32212"}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]

autodoc_mock_imports = [""]
autoclass_content = "both"
autosummary_generate = True

autodoc_pydantic_model_show_json = False

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
