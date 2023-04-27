from typing import List

from pandas_profiling.config import Settings
from pandas_profiling.model.transformations import TransformationData
from pandas_profiling.report.presentation.core.container import Container
from pandas_profiling.report.presentation.core.html import HTML
from pandas_profiling.report.structure.model_render import render_model


def _get_transformation_info(config: Settings, transformation_data: TransformationData):
    transform_description = HTML(
        content=transformation_data.transform_desc,
    )
    return Container(
        [transform_description],
        name="Used transformation: {}".format(transformation_data.transform_name),
        sequence_type="grid",
        anchor_id="transform_desc_{}".format(transformation_data.transform_name),
    )


def render_transformations_module(
    config: Settings, transformations_data: List[TransformationData]
) -> Container:
    items = []
    if len(transformations_data) == 0:
        items.append(
            HTML(
                content="There are no transformations, that would improve base model.",
                anchor_id="transform_tab_empty",
                name="transform_tab_empty",
            )
        )
        return Container(
            items,
            name="Transformations",
            sequence_type="accordion",
            anchor_id="transform_module",
        )

    for transform_data in transformations_data:
        transform_info = _get_transformation_info(config, transform_data)
        model_evaluation = render_model(
            config, transform_data.model_data, name=transform_data.transform_name
        )
        one_transform = Container(
            [transform_info, model_evaluation],
            name=transform_data.col_name,
            sequence_type="named_list",
            anchor_id="transform_tab_{}".format(transform_data.col_name),
        )

        items.append(one_transform)

    return Container(
        items,
        name="Transformations",
        sequence_type="tabs",
        anchor_id="transform_module",
    )
