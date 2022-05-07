---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: ''

---

<!--- Provide a general summary of the issue in the Title above -->

## Current Behaviour
<!--- Tell us what happens instead of the expected behavior -->

## Expected Behaviour
<!--- Tell us what should happen -->

## Steps to Reproduce

### Data description, sample and/or characteristics

### Code to reproduce

```python
import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_parquet(r"<file>")
report = ProfileReport(df, title="bug report")
report.to_file("report.html")
```

### Context: Environment and Version information

- pandas-profiling version: X
- Python version (fill out): 3.X
- Dependencies (e.g. `pip` or `conda`, [help](https://pandas-profiling.ydata.ai/docs/master/rtd/pages/support.html))
- Environment (e.g. Command line, IDE (PyCharm, Spyder, IDLE etc.), Jupyter Notebook (Colab or local)): X
- Operating system: X

## Proposed solution
<!--- Not obligatory, but suggest a fix/reason for the bug, -->


## Checklist

Please complete the checklist below to ensure the bug report is helpful and can be addressed effectively:

- [ ] All (relevant) sections above are filled out.
- [ ] The problem is reproducible from this bug report. [This guide](http://matthewrocklin.com/blog/work/2018/02/28/minimal-bug-reports) can help to craft a minimal bug report.
- [ ] The issue has not been resolved by the entries listed under [Frequent Issues](https://pandas-profiling.ydata.ai/docs/master/rtd/pages/support.html#frequent-issues).
- [ ] The bug report is formatted according to [the guidelines](https://pandas-profiling.ydata.ai/docs/master/rtd/pages/support.html#issue-formatting).

Tips:
- Help for writing better bug reports is available in the [documentation](https://pandas-profiling.ydata.ai/docs/master/rtd/pages/support.html).
- If the description consists of multiple non-related bugs, you are encouraged to create separate issues.
