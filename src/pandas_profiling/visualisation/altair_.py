import uuid

import altair as alt

from pandas_profiling.config import config
from pandas_profiling.report.presentation.core import HTML
from pandas_profiling.visualisation.plot import PlotRegister, render_plot


def render_vega_json(varid):
    html = f"""
    <div id="vis{varid}"></div>

    <script type="text/javascript">
      var spec = "{varid}.json";
      vegaEmbed('#vis{varid}', spec, {{"actions": false, "renderer": "svg"}}).then(function(result) {{}}).catch(console.error);
    </script>"""
    return html


@render_plot.register(alt.Chart)
def _(plot_obj: alt.Chart, name, *args, **kwargs):
    interactive = config["plot"]["altair"]["interactive"].get(bool)

    if interactive:
        plot_obj = plot_obj.interactive()
    plot_obj = plot_obj.configure_view(strokeWidth=0)

    # TODO: width, height by renderer
    # plot_obj = plot_obj.properties(width=210, height=150)

    # TODO: assets folder
    idx = uuid.uuid4().hex.lower()
    idx = f"altair{idx}"
    plot_obj.save(f"{idx}.json")

    return HTML(
        render_vega_json(f"{idx}"),
        name=name,
        anchor_id=f"{idx}",
    )


@PlotRegister.register()
def histogram(data) -> alt.Chart:
    vc = data.reset_index(name="counts")

    return (
        alt.Chart(vc)
        .mark_bar(color="#337ab7")
        .encode(x="index", y="counts", tooltip=["index", "counts"])
    )


@PlotRegister.register()
def bar(data) -> alt.Chart:
    return histogram(data)


@PlotRegister.register()
def correlation_matrix(data, vmin) -> alt.Chart:
    cor_data = (
        data.stack()
        .reset_index()  # The stacking results in an index on the correlation values, we need the index as normal columns for Altair
        .rename(
            columns={0: "correlation", "level_0": "variable1", "level_1": "variable2"}
        )
    )
    cor_data["correlation_label"] = cor_data["correlation"].map(
        "{:.2f}".format
    )  # Round to 2 decimal

    # mark_square
    base = (
        alt.Chart(cor_data)
        .encode(
            x=alt.X(
                "variable2:O", axis=alt.Axis(title=None, domainOpacity=0, gridOpacity=0)
            ),
            y=alt.Y(
                "variable1:O", axis=alt.Axis(title=None, domainOpacity=0, gridOpacity=0)
            ),
        )
        .mark_rect(
            # size=120
        )
        .encode(
            color=alt.Color(
                "correlation:Q",
                scale=alt.Scale(scheme="redblue", domain=[vmin, 1]),
                legend=alt.Legend(
                    title=None,
                    gradientLength=500,
                    gradientThickness=30,
                ),
            ),
            size="correlation:Q",
            tooltip=[alt.Tooltip("correlation_label:O", title="Coefficient")],
        )
        .properties(
            width=500,
            height=500
            # width=alt.Step(80), height=alt.Step(80)
        )
    )

    # text = base.mark_text(
    #     size=30
    # ).encode(
    #     text=alt.Text('correlation', format=".2f"),
    #     color=alt.condition(
    #         "datum.correlation > 0.5",
    #         alt.value('white'),
    #         alt.value('black')
    #     )
    # )

    # base += text

    return base


@PlotRegister.register()
def scatter(data, x_label, y_label) -> alt.Chart:
    base = (
        alt.Chart(data)
        .mark_circle(size=60, color="#337ab7")
        .encode(x=x_label, y=y_label, tooltip=[x_label, y_label])
    )
    return base


@PlotRegister.register()
def heatmap(data, x_label, y_label) -> alt.Chart:
    base = (
        alt.Chart(data)
        .mark_circle(size=60)
        .encode(x=x_label, y=y_label, tooltip=[x_label, y_label])
    )
    return base


@PlotRegister.register()
def plot_stacked_bar(data) -> alt.Chart:
    base = (
        alt.Chart(data)
        .mark_bar(color="#337ab7")
        .encode(
            x=data.columns[0],
            y=f"count({data.columns[1]}):Q",
            color=data.columns[0],
            column=data.columns[1],
        )
    )
    return base


# @PlotRegister.register()
# def plot_boolean_matrix(data) -> alt.Chart:
#     data = (
#         data.stack()
#         .reset_index()
#         .rename(columns={0: "value", "level_0": "row", "level_1": "variable"})
#     )
#
#     return (
#         alt.Chart(data)
#         .mark_rect(height=3)
#         .encode(
#             y=alt.Y("row:O", axis=alt.Axis(values=list(range(1, 74, 5)))),
#             x="variable:O",
#             color=alt.Color("value:Q", scale=alt.Scale(range=["black", "white"])),
#         )
#         .properties(height=alt.Step(3), width=500)
#     )
#
#
# @PlotRegister.register()
# def plot_boolean_bar(data) -> alt.Chart:
#     # data = data.stack().reset_index().rename(columns={0: 'value', 'level_0': 'row', 'level_1': 'variable'})
#
#     return (
#         alt.Chart(data)
#         .mark_bar(color="black")
#         .encode(
#             y=alt.Y("sum(value):Q"),
#             x="variable:O",
#         )
#         .properties(
#             # height=alt.Step(3),
#             width=500
#         )
#     )


@PlotRegister.register()
def qq_plot(data, distribution="norm") -> alt.Chart:
    base = (
        alt.Chart(data)
        .transform_quantile("u", step=0.01, as_=["p", "v"])
        .transform_calculate(
            # uniform='quantileUniform(datum.p)',
            normal="quantileNormal(datum.p)"
        )
        .mark_point()
        .encode(alt.Y("v:Q"))
    )
    # base.encode(x='uniform:Q') |
    return base.encode(x="normal:Q")


@PlotRegister.register()
def pie_chart(data):
    # raise NotImplementedError("pie chart not supported by altair")
    return histogram(data)


@PlotRegister.register()
def boxplot(data):
    return (
        alt.Chart(data)
        .mark_boxplot()
        .encode(
            # x='species:O',
            # y=alt.Y('culmen_length_mm:Q', scale=alt.Scale(zero=False)),
            color=alt.Color("species")
        )
    )
