from pandas_profiling.model import summary_methods as pps
from pandas_profiling.model import typeset as ppt
from pandas_profiling.model.base import get_counts


class HandlerMixin:
    def __init__(self, **kwargs):
        if kwargs:
            raise TypeError(f"Got an unexpected keyword argument(s) {kwargs}")


class SummaryHandler(HandlerMixin):
    def __init__(self, summary_map, **kwargs):
        super().__init__(**kwargs)
        self.summary_map = summary_map

    def summarize(self, series, dtype=None, series_description={}):
        if dtype is None:
            dtype = self.typeset.infer_type(series)

        return self.summary_map[dtype](series, series_description)


class RenderHandler(HandlerMixin):
    def __init__(self, render_map, **kwargs):
        super().__init__(**kwargs)
        self.render_map = render_map

    def render(self, template, dtype):
        return self.render_map[dtype](template)


class MessageHandler(HandlerMixin):
    def __init__(self, message_map, **kwargs):
        super().__init__(**kwargs)
        self.message_map = message_map


class ProfilingHandler(SummaryHandler, RenderHandler, MessageHandler):
    def __init__(self, typeset, **kwargs):
        super().__init__(**kwargs)
        self.typeset = typeset

    def get_var_type(self, series):
        # TODO: Refactor into two pieces, summaries and type detection
        series_description = get_counts(series)
        series_description["type"] = self.typeset.infer_type(series)
        return series_description


# TODO: Counts?
def default_handler():
    from pandas_profiling.report.structure.variables import (
        render_boolean,
        render_categorical,
        render_complex,
        render_date,
        render_file,
        render_generic,
        render_image,
        render_path,
        render_real,
        render_url,
    )

    typeset = ppt.ProfilingTypeSet()

    summary_map = {
        ppt.Bool: pps.describe_boolean_1d,
        ppt.Numeric: pps.describe_numeric_1d,
        ppt.Date: pps.describe_date_1d,
        ppt.Category: pps.describe_categorical_1d,
        ppt.URL: pps.describe_url_1d,
        ppt.Path: pps.describe_path_1d,
        ppt.Image: pps.describe_image_1d,
        ppt.File: pps.describe_file_1d,
        ppt.Complex: pps.describe_complex_1d,
        ppt.Unsupported: pps.describe_unsupported,
    }

    render_map = {
        ppt.Bool: render_boolean,
        ppt.Numeric: render_real,
        ppt.Complex: render_complex,
        ppt.Date: render_date,
        ppt.Category: render_categorical,
        ppt.URL: render_url,
        ppt.Path: render_path,
        ppt.File: render_file,
        ppt.Image: render_image,
        ppt.Unsupported: render_generic,
    }

    return ProfilingHandler(
        typeset, summary_map=summary_map, render_map=render_map, message_map={}
    )
