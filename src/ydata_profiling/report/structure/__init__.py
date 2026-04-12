"""Data structure for the report"""
from typing import Callable, Dict


def get_render_map() -> Dict[str, Callable]:
    """Get the mapping of variable types to their render functions.

    This function was moved from model.handler to report.structure to eliminate
    the reverse dependency from model layer to report layer.

    Returns:
        Dictionary mapping type names to render functions.
    """
    import ydata_profiling.report.structure.variables as render_algorithms

    render_map = {
        "Boolean": render_algorithms.render_boolean,
        "Numeric": render_algorithms.render_real,
        "Complex": render_algorithms.render_complex,
        "Text": render_algorithms.render_text,
        "DateTime": render_algorithms.render_date,
        "Categorical": render_algorithms.render_categorical,
        "URL": render_algorithms.render_url,
        "Path": render_algorithms.render_path,
        "File": render_algorithms.render_file,
        "Image": render_algorithms.render_image,
        "Unsupported": render_algorithms.render_generic,
        "TimeSeries": render_algorithms.render_timeseries,
    }

    return render_map
