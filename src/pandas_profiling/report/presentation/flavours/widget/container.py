from ipywidgets import widgets

from pandas_profiling.report.presentation.core.container import Container
from pandas_profiling.report.presentation.core.renderable import Renderable


def get_name(item: Renderable):
    if hasattr(item, "name"):
        return item.name
    else:
        return item.anchor_id


def get_tabs(items):
    children = []
    titles = []
    for item in items:
        children.append(item.render())
        titles.append(get_name(item))

    tab = widgets.Tab()
    tab.children = children
    for id, title in enumerate(titles):
        tab.set_title(id, title)
    return tab


def get_list(items):
    return widgets.VBox([item.render() for item in items])


def get_named_list(items):
    return widgets.VBox(
        [
            widgets.VBox(
                [widgets.HTML(f"<strong>{get_name(item)}</strong>"), item.render()]
            )
            for item in items
        ]
    )


def get_row(items):
    if len(items) == 1:
        layout = widgets.Layout(width="100%", grid_template_columns="100%")
    elif len(items) == 2:
        layout = widgets.Layout(width="100%", grid_template_columns="50% 50%")
    elif len(items) == 3:
        layout = widgets.Layout(width="100%", grid_template_columns="25% 25% 50%")
    elif len(items) == 4:
        layout = widgets.Layout(width="100%", grid_template_columns="25% 25% 25% 25%")
    else:
        raise ValueError("Layout undefined for this number of columns")

    return widgets.GridBox([item.render() for item in items], layout=layout)


def get_batch_grid(items, batch_size, titles):
    layout = widgets.Layout(
        width="100%",
        grid_template_columns=" ".join([f"{int(100 / batch_size)}%"] * batch_size),
    )
    return widgets.GridBox([item.render() for item in items], layout=layout)


def get_accordion(items):
    children = []
    titles = []
    for item in items:
        children.append(item.render())
        titles.append(get_name(item))

    accordion = widgets.Accordion(children=children)
    for id, title in enumerate(titles):
        accordion.set_title(id, title)

    return accordion


class WidgetContainer(Container):
    def render(self):
        if self.sequence_type == "list":
            widget = get_list(self.content["items"])
        elif self.sequence_type == "named_list":
            widget = get_named_list(self.content["items"])
        elif self.sequence_type in ["tabs", "sections", "select"]:
            widget = get_tabs(self.content["items"])
        elif self.sequence_type == "accordion":
            widget = get_accordion(self.content["items"])
        elif self.sequence_type == "grid":
            widget = get_row(self.content["items"])
        elif self.sequence_type == "batch_grid":
            widget = get_batch_grid(
                self.content["items"],
                self.content["batch_size"],
                self.content.get("titles", True),
            )
        else:
            raise ValueError("widget type not understood", self.sequence_type)

        return widget
