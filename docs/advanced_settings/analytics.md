# Analytics & Telemetry

## Overview

`ydata-profiling` is a powerful library designed to generate profile reports from pandas and Spark Dataframe objects. 
As part of our ongoing efforts to improve user experience and functionality, `ydata-profiling` 
includes a telemetry feature. This feature collects anonymous usage data, helping us understand how the
library is used and identify areas for improvement.

The primary goal of collecting telemetry data is to:

- Enhance the functionality and performance of the ydata-profiling library
- Prioritize new features based on user engagement
- Identify common issues and bugs to improve overall user experience

### Data Collected

The telemetry system collects non-personal, anonymous information such as:

- Python version
- `ydata-profiling` version
- Frequency of use of `ydata-profiling` features
- Errors or exceptions thrown within the library

## Disabling usage analytics

We respect your choice to not participate in our telemetry collection. If you prefer to disable telemetry, you can do so
by setting an environment variable on your system. Disabling telemetry will not affect the functionality 
of the ydata-profiling library, except for the ability to contribute to its usage analytics.


### Set an Environment Variable

Open your terminal or command prompt and set the YDATA_PROFILING_NO_ANALYTICS environment variable to false.

````python
    import os 
    
    os.environ['YDATA_PROFILING_NO_ANALYTICS'] = 'True'
````

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=baa0e45f-0c03-4190-9646-9d8ea2640ba2" />
