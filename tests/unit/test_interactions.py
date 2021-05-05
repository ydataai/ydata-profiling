import numpy as np
import pandas as pd

from pandas_profiling import ProfileReport


def test_interactions_target():
    n_rows = 10
    n_columns = 50
    n_targets = 2

    df = pd.DataFrame(
        np.random.randint(0, 1000, size=(n_rows, n_columns)),
        columns=[f"column_{c}" for c in range(n_columns)],
    )
    targets = [f"column_{target}" for target in range(0, n_targets)]

    profile = ProfileReport(
        df, minimal=True, interactions={"continuous": True, "targets": targets}
    )

    total = sum(
        [len(v.keys()) for k, v in profile.get_description()["scatter"].items()]
    )
    assert total == n_targets * n_columns
