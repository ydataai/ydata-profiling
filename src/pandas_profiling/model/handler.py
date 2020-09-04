from pandas_profiling.model import typeset as ppt


def get_render_map():
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

    render_map = {
        ppt.Boolean: render_boolean,
        ppt.Numeric: render_real,
        ppt.Complex: render_complex,
        ppt.DateTime: render_date,
        ppt.Categorical: render_categorical,
        ppt.URL: render_url,
        ppt.Path: render_path,
        ppt.File: render_file,
        ppt.Image: render_image,
        ppt.Unsupported: render_generic,
    }

    return render_map
