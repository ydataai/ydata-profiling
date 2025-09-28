"""
Jinja2 internationalization extension for ydata-profiling
"""
from jinja2 import nodes
from jinja2.ext import Extension
from ydata_profiling.i18n import _

class I18nExtension(Extension):
    """Jinja2 extension for internationalization"""

    tags = {'trans'}

    def __init__(self, environment):
        super().__init__(environment)
        environment.globals['_'] = _
        environment.globals['gettext'] = _
        environment.filters['trans'] = self.translate_filter

    def translate_filter(self, key, **kwargs):
        """Filter for translating keys in templates"""
        return _(key, **kwargs)

    def parse(self, parser):
        """Parse trans tag for {% trans %} syntax"""
        lineno = next(parser.stream).lineno
        key = parser.parse_expression()
        return nodes.Output([
            nodes.Call(
                nodes.Name('_', 'load'),
                [key],
                []
            )
        ]).set_lineno(lineno)