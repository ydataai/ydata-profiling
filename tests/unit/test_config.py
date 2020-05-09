from multiprocessing import Pool

import pandas as pd

from pandas_profiling import ProfileReport


def profile_report(kwargs):
    profile = ProfileReport(**kwargs)
    return profile.description_set["analysis"]["title"], profile.to_json()


def test_config_mutiprocess():
    df = pd.DataFrame(
        {"a": [1, 2, 3, 1, 1, 1], "b": [1, 2, 3, 4, 5, 6], "c": [1, 2, 3, 4, 5, 6]}
    )
    pool = Pool(processes=2)

    ret0 = pool.apply_async(
        profile_report, args=({"df": df, "minimal": True, "title": "minimal-report"},)
    )
    ret1 = pool.apply_async(
        profile_report, args=({"df": df, "minimal": False, "title": "default-report"},)
    )

    pool.close()
    pool.join()

    profile0_title, profile0_json = ret0.get()
    profile1_title, profile1_json = ret1.get()

    assert profile0_json != profile1_json
    assert profile0_title == "minimal-report"
    assert profile1_title == "default-report"
