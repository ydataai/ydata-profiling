from pandas_profiling.visualisation.plot import (
    missing_bar,
    missing_dendrogram,
    missing_heatmap,
    missing_matrix,
    render_plot,
)


def get_missing_items(summary) -> list:
    """Return the missing diagrams

    Args:
        summary: the dataframe summary

    Returns:
        A list with the missing diagrams
    """

    fns = {
        "bar": missing_bar,
        "matrix": missing_matrix,
        "heatmap": missing_heatmap,
        "dendrogram": missing_dendrogram,
    }

    items = []
    for key, item in summary["missing"].items():
        items.append(
            render_plot(
                fns[item["matrix"]](item["data"]),
                alt=item["name"],
                name=item["name"],
                anchor_id=key,
            )
        )

    return items
