from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency


@dataclass
class ConfMatrixData:
    """Class for confusion matrix in absolute and relative numbers.

    Args:
        absolute_counts (pd.DataFrame): Absolute counts of missing.
        relative_counts (pd.DataFrame): Relative counts of missing. Row sums at 100%.
    """

    absolute_counts: pd.DataFrame
    relative_counts: pd.DataFrame
    _p_value: Optional[float] = None
    _expected_counts: Optional[np.ndarray] = None

    @property
    def p_value(self) -> float:
        """P value from chi-square test of variables from contingency table."""
        if not self._p_value:
            self._p_value = chi2_contingency(self.absolute_counts, correction=False)[1]
        return self._p_value

    @property
    def expected_counts(self):
        """Matrix of expected frequencies, based on the marginal sums of the table."""
        if not self._expected_counts:
            self._expected_counts = chi2_contingency(self.absolute_counts)[3]
        return self._expected_counts

    @property
    def plot_labels(self) -> list:
        """Labels for confusion matrix.
        Contain relative count and absolute count of values."""
        flat_abs = self.absolute_counts.values.flatten()
        flat_rel = self.relative_counts.values.flatten()
        labels = []
        for abs, rel in zip(flat_abs, flat_rel):
            labels.append("{0:.2%}\n{1}".format(rel, abs))
        return np.asarray(labels).reshape(self.absolute_counts.shape)
