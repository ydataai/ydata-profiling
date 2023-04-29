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
                "alert": config.model.evaluation_metric == "accuracy",
            },
            {
                "name": "Precision (%)",
                "value": fmt_percent(model_evaluation.precision),
                "alert": config.model.evaluation_metric == "precision",
            },
            {
                "name": "Recall (%)",
                "value": fmt_percent(model_evaluation.recall),
                "alert": config.model.evaluation_metric == "recall",
            },
            {
                "name": "F1 score (%)",
                "value": fmt_percent(model_evaluation.f1_score),
                "alert": config.model.evaluation_metric == "f1_score",
            },
        ],
        style=config.html.style,
        name="Model evaluation",
    )


def _get_model_setting_table(config: Settings, model_data: ModelData):
    return Table(
        [
            {
                "name": "Used model",
                "value": model_data.model_source,
            },
            {
                "name": "Boosting type",
                "value": model_data.boosting_type,
            },
            {
                "name": "Maximum tree depth",
                "value": fmt_number(config.model.max_depth),
            },
            {
                "name": "Number of boosted trees",
                "value": fmt_number(config.model.n_estimators),
            },
            {
                "name": "Maximum tree leaves",
                "value": fmt_number(config.model.num_leaves),
            },
            {
                "name": "Model seed",
                "value": fmt_number(config.model.model_seed),
            },
        ],
        style=config.html.style,
        name="Model setting",
    )


def _get_train_test_setting_table(config: Settings, model_data: ModelData):
    return Table(
        [
            {
                "name": "Train test split policy",
                "value": model_data.train_test_split_policy,
            },
            {
                "name": "Test size (%)",
                "value": fmt_percent(config.model.test_size),
            },
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
        name="Train test setting",
    )


def _get_feature_importances(config: Settings, model_data: ModelData):
    records = []
    for importnace, feature in model_data.get_feature_importances():
        if importnace == 0:
            break
        records.append(
            {
                "name": feature,
                "value": fmt_number(importnace),
            }
        )

    return Table(
        records,
        style=config.html.style,
        name="Feature importances",
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

    evaluation_tab = _get_evaluation_table(config, model_evaluation)
    conf_matrix = Image(
        plot_conf_matrix(config, model_evaluation.confusion_matrix),
        image_format=config.plot.image_format,
        alt="Predict confusion matrix",
        anchor_id="{}_predict_conf_matrix".format(name),
        name=name,
    )
    top_section = Container(
        [evaluation_tab, conf_matrix],
        sequence_type="grid",
        name="Model info top",
    )

    bottom_items = []
    bottom_items.append(_get_model_setting_table(config, model_data))
    bottom_items.append(_get_train_test_setting_table(config, model_data))
    bottom_items.append(_get_feature_importances(config, model_data))
    bottom_section = Container(
        bottom_items,
        sequence_type="batch_grid",
        name="Model info bottom",
        batch_size=len(bottom_items),
        titles=False,
    )

    return Container(
        [top_section, bottom_section],
        sequence_type="list",
        name="Model info",
        anchor_id="{}_model".format(name),
    )


def render_model_module(config: Settings, model_module: ModelModule) -> Container:
    items = []

    def_model_tab = render_model(config, model_module.default_model, "Base model")
    items.append(def_model_tab)

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
