from typing import Any, Dict

from pandas_profiling.config import Settings
from pandas_profiling.model.description_variable import TextDescriptionSupervised
from pandas_profiling.report.formatters import fmt, fmt_bytesize, fmt_percent
from pandas_profiling.report.presentation.core import (
    Container,
    FrequencyTable,
    Image,
    LogOddsTable,
    Table,
)
from pandas_profiling.report.presentation.log_odds_utils import log_odds_table
from pandas_profiling.report.structure.variables.base_render import BaseRenderVariable
from pandas_profiling.report.structure.variables.render_categorical import (
    _get_n,
    freq_table,
    render_categorical_frequency,
    render_categorical_length,
)
from pandas_profiling.visualisation.plot import plot_word_cloud


class RenderText(BaseRenderVariable):
    def __get_wordcloud(self, mini=True):
        """Render word cloud.

        Args:
            mini (bool): If plot is normal size, or mini size
        """
        if mini:
            alt = "Mini wordcloud"
        else:
            alt = "Wordcloud"

        return Image(
            plot_word_cloud(self.config, self.summary["plot_description"], mini),
            image_format=self.config.plot.image_format,
            name="word cloud",
            alt=alt,
        )

    def _get_top(self) -> Container:
        """Render top of string variable.

        Contains
        - basic info
        - table with information about missing values
        - word cloud graph"""
        top_items = []
        top_items.append(self._get_info())
        table = Table(
            [
                {
                    "name": "Distinct",
                    "value": fmt(self.summary["n_distinct"]),
                    "alert": "n_distinct" in self.summary["alert_fields"],
                },
                {
                    "name": "Distinct (%)",
                    "value": fmt_percent(self.summary["p_distinct"]),
                    "alert": "p_distinct" in self.summary["alert_fields"],
                },
                {
                    "name": "Missing",
                    "value": fmt(self.summary["n_missing"]),
                    "alert": "n_missing" in self.summary["alert_fields"],
                },
                {
                    "name": "Missing (%)",
                    "value": fmt_percent(self.summary["p_missing"]),
                    "alert": "p_missing" in self.summary["alert_fields"],
                },
                {
                    "name": "Memory size",
                    "value": fmt_bytesize(self.summary["memory_size"]),
                    "alert": False,
                },
            ],
            style=self.config.html.style,
        )
        top_items.append(table)

        # we dont have log odds plot -> plot distribution if dist or logodds enabled
        if self.config.vars.text.words and (
            self.config.report.vars.distribution_on_top
            or self.config.report.vars.log_odds_on_top
        ):
            top_items.append(self.__get_wordcloud(True))
        return Container(top_items, sequence_type="grid")

    def _get_overview(self) -> Container:
        """Render overview container.

        Contains
        - string length
        - unique statistic
        - sample of data"""
        overview_items = []
        if self.config.vars.text.length:
            length_table, length_histo = render_categorical_length(
                self.config, self.summary, self.summary["varid"]
            )
            overview_items.append(length_table)

        unique_stats = render_categorical_frequency(
            self.config, self.summary, self.summary["varid"]
        )
        overview_items.append(unique_stats)

        if not self.config.vars.cat.redact:
            rows = ("1st row", "2nd row", "3rd row", "4th row", "5th row")

            if isinstance(self.summary["first_rows"], list):
                sample = Table(
                    [
                        {
                            "name": name,
                            "value": fmt(value),
                            "alert": False,
                        }
                        for name, *value in zip(rows, *self.summary["first_rows"])
                    ],
                    name="Sample",
                    style=self.config.html.style,
                )
            else:
                sample = Table(
                    [
                        {
                            "name": name,
                            "value": fmt(value),
                            "alert": False,
                        }
                        for name, value in zip(rows, self.summary["first_rows"])
                    ],
                    name="Sample",
                    style=self.config.html.style,
                )
            overview_items.append(sample)
        return Container(
            overview_items,
            name="Overview",
            anchor_id="{}overview".format(self.summary["varid"]),
            sequence_type="batch_grid",
            batch_size=len(overview_items),
            titles=False,
        )

    def _get_words(self) -> Container:
        """Render words container.

        Contains
        - frequency table of words
        - word map"""
        items = []

        if isinstance(self.summary["plot_description"], TextDescriptionSupervised):
            lo_table = log_odds_table(
                self.summary["plot_description"], self.config.n_freq_table_max
            )
            items.append(
                LogOddsTable(
                    lo_table,
                    name="Log odds words with Beta smoothing. alpha + beta = {}".format(
                        self.config.vars.base.smoothing_parameter
                    ),
                    anchor_id="{}cwo".format(self.summary["varid"]),
                    redact=self.config.vars.cat.redact,
                )
            )
        else:
            woc = freq_table(
                freqtable=self.summary["word_counts"],
                n=_get_n(self.summary["word_counts"]),
                max_number_to_print=10,
            )
            fqwo = FrequencyTable(
                woc,
                name="Common words",
                anchor_id="{}cwo".format(self.summary["varid"]),
                redact=self.config.vars.cat.redact,
            )
            items.append(fqwo)

        items.append(self.__get_wordcloud(False))

        return Container(
            items,
            name="Words",
            anchor_id="{}word".format(self.summary["varid"]),
            sequence_type="named_list",
        )

    def _get_bottom(self) -> Container:
        """Render bottom section of variable.

        Contains
        - overview container
        - words container"""
        bottom_items = []
        bottom_items.append(self._get_overview())
        if self.config.vars.text.words:
            bottom_items.append(self._get_words())

        return Container(
            bottom_items,
            sequence_type="tabs",
            anchor_id="{}bottom".format(self.summary["varid"]),
        )


def render_text(config: Settings, summary: Dict[str, Any]):
    """Return render for Text variable.

    Args:
        config (Settings): Setting of profile report.
        summary (dict): Summary of rendered variable.
    """
    render = RenderText(config, summary).render()
    return render
