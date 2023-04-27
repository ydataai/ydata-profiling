from pandas_profiling.config import Settings
from pandas_profiling.model.model import ModelData, ModelEvaluation, ModelModule
from pandas_profiling.report.formatters import fmt_number, fmt_percent
from pandas_profiling.report.presentation.core import Image
from pandas_profiling.report.presentation.core.container import Container
from pandas_profiling.report.presentation.core.html import HTML
from pandas_profiling.report.presentation.core.table import Table
from pandas_profiling.visualisation.plot import plot_conf_matrix


def _get_evaluation_table(config: Settings, model_evaluation: ModelEvaluation):
    return Table(
        [
            {
                "name": "Accuracy (%)",
                "value": fmt_percent(model_evaluation.accuracy),
            },
            {
                "name": "Precision (%)",
                "value": fmt_percent(model_evaluation.precision),
            },
            {
                "name": "Recall (%)",
                "value": fmt_percent(model_evaluation.recall),
            },
            {
                "name": "F1 score (%)",
                "value": fmt_percent(model_evaluation.f1_score),
            },
        ],
        style=config.html.style,
        name="Model evaluation",
    )


def _get_train_test_table(config: Settings, model_data: ModelData):
    return Table(
        [
            {
                "name": "Train records count",
                "value": fmt_number(model_data.train_records),
            },
            {
                "name": "Test records count",
                "value": fmt_number(model_data.test_records),
            },
        ],
        style=config.html.style,
        name="Train-test info",
    )


def render_model(config: Settings, model_data: ModelData, name: str) -> Container:
    """Render one model information.

    Args:
        config (Settings): Report configuration
        model_data (ModelData): Data about model
        name (str): Name of tab

    Returns:
        Container: Renderable description of one model.
    """
    model_evaluation = model_data.evaluate()

    items = []

    items.append(_get_evaluation_table(config, model_evaluation))
    items.append(_get_train_test_table(config, model_data))

    conf_matrix = Image(
        plot_conf_matrix(config, model_evaluation.confusion_matrix),
        image_format=config.plot.image_format,
        alt="Predict confusion matrix",
        anchor_id="{}_predict_conf_matrix".format(name),
        name=name,
    )
    items.append(conf_matrix)

    return Container(
        items,
        sequence_type="grid",
        name=model_data.model_name,
    )


def render_model_module(config: Settings, model_module: ModelModule) -> Container:
    items = []

    def_model_tab = render_model(config, model_module.default_model, "Base model")
    items.append(
        Container(
            [def_model_tab],
            name="Base model",
            sequence_type="named_list",
            anchor_id="model_tab_base_model",
        )
    )

    if model_module.transformed_model:
        trans_model_tab = render_model(
            config,
            model_module.transformed_model,
            "Model with transformed data",
        )
        items.append(trans_model_tab)

    return Container(
        items,
        name="Model",
        sequence_type="tabs",
        anchor_id="model_module",
    )
