from typing import Union

import pandas as pd
from numpy import log2
from scipy.stats import entropy


def column_imbalance_score(
    value_counts: pd.Series, n_classes: int
) -> Union[float, int]:
    """column_imbalance_score

    The class balance score for categorical and boolean variables uses entropy to calculate a  bounded score between 0 and 1.
    A perfectly uniform distribution would return a score of 0, and a perfectly imbalanced distribution would return a score of 1.

    When dealing with probabilities with finite values (e.g categorical), entropy is maximised the ‘flatter’ the distribution is. (Jaynes: Probability Theory, The Logic of Science)
    To calculate the class imbalance, we calculate the entropy of that distribution and the maximum possible entropy for that number of classes.
    To calculate the entropy of the 'distribution' we use value counts (e.g frequency of classes) and we can determine the maximum entropy as log2(number of classes).
    We then divide the entropy by the maximum possible entropy to get a value between 0 and 1 which we then subtract from 1.

    Args:
        value_counts (pd.Series): frequency of each category
        n_classes (int): number of classes

    Returns:
        Union[float, int]: float or integer bounded between 0 and 1 inclusively
    """
    # return 0 if there is only one class (when entropy =0) as it is balanced.
    # note that this also prevents a zero division error with log2(n_classes)
    if n_classes > 1:
        # casting to numpy array to ensure correct dtype when a categorical integer
        # variable is evaluated
        value_counts = value_counts.to_numpy(dtype=float)
        return 1 - (entropy(value_counts, base=2) / log2(n_classes))
    return 0
