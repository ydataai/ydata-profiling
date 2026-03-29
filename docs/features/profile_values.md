# Accessing profile files

ydata-profiling allows you to access and export the computed profile data 
programmatically, beyond just the HTML report.

## JSON output structure

You can export the full profile as a JSON file:
```python
import pandas as pd
from ydata_profiling import ProfileReport

df = pd.read_csv("your_data.csv")
profile = ProfileReport(df, title="My Report")
profile.to_file("report.json")
```

The JSON output contains all computed statistics organized by variable name,
including type, missing values, descriptive statistics, and correlations.

## Univariate variables statistics through description_set

You can access per-variable statistics directly in Python via `description_set`:
```python
description = profile.get_description()
# Access stats for a specific variable
print(description.variables["your_column_name"])
```

This returns a dictionary of computed metrics for each variable — type,
missing count, distinct count, mean, std, quantiles, and more.

## Correlation matrices through description_set

Correlation matrices computed during profiling are also accessible:
```python
description = profile.get_description()
# Pearson correlation matrix
print(description.correlations["pearson"])
```

Available correlation keys depend on your configuration but typically include
`pearson`, `spearman`, `kendall`, and `cramers`.