import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np
df = pd.DataFrame([1, 1, np.nan], columns=["a"])

profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)

print(profile.to_json())
