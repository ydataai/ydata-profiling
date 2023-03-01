from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from multimethod import multimethod
from pandas_profiling.config import Target


@dataclass
class TargetDescription(metaclass=ABCMeta):
    """Description for target column."""

    series: Any
    series_binary: Any
    config: Target
    name: str
    description: Dict[str, Any]
    positive_values: List[str]
    negative_values: List[str]

    def __init__(
        self,
        target_config: Target,
        series: Any,
    ) -> None:
        self.series = series
        self.config = target_config
        self.name = target_config.col_name
        self.description = {}
        self.positive_values, self.negative_values = self._infer_target_values()
        self.series_binary = self._get_bin_target()
        self._update_description_base()

    @property
    def bin_positive(self) -> int:
        """Positive value for series_binary."""
        return 1

    @property
    def bin_negative(self) -> int:
        """Negative value for series_binary."""
        return 0

    @abstractmethod
    def _infer_target_values(self) -> Tuple[List[str], List[str]]:
        """Infer positive and negative values in target column.

        Returns:
            positive, negative (Tuple[List[str], List[str]]):
                Positive and negative values.
        """
        pass

    @abstractmethod
    def _get_bin_target(self) -> Any:
        """Create binary target from column and positive/negative values.
        Positive values replace with 1, negative with -1."""
        pass

    @abstractmethod
    def _get_advanced_description(self) -> Dict[str, Any]:
        """Update description for target variable.
        Get target mean."""
        pass

    @property
    @abstractmethod
    def n_positive_vals(self) -> int:
        """Count of positive values in series."""
        pass

    @property
    @abstractmethod
    def p_positive_vals(self) -> float:
        """Percentage of positive values in series."""
        pass

    @property
    @abstractmethod
    def n_negative_vals(self) -> int:
        """Count of negative values in series."""
        pass

    @property
    @abstractmethod
    def p_negative_vals(self) -> float:
        """Percentage of negative values in series."""
        pass

    def _update_description_base(self) -> None:
        """Update description.
        Add positive and negative values."""
        _desc = {}
        _desc["target"] = True
        _desc["positive_vals"] = self.positive_values
        _desc["n_positive_vals"] = self.n_positive_vals
        _desc["p_positive_vals"] = self.p_positive_vals
        _desc["negative_vals"] = self.negative_values
        _desc["n_negative_vals"] = self.n_negative_vals
        _desc["p_negative_vals"] = self.p_negative_vals
        _desc.update(self._get_advanced_description())

        self.description.update(_desc)


@multimethod
def describe_target(
    config: Target,
    data_frame: Any,
) -> TargetDescription:
    """Generate target description."""
    raise NotImplementedError()
