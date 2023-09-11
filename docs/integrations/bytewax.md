# Profiling for streaming data                                         

## About Bytewax                                                        

[Bytewax](https://github.com/bytewax/bytewax) is an OSS stream
processing framework designed specifically for Python developers.    
It allows users to build streaming data pipelines and real-time
applications with capabilities similar to Flink, Spark, and Kafka
Streams, while providing a friendly and familiar interface and 100%
compatibility with the Python ecosystem.

## Stream processing with Bytewax and ydata-profiling      

Data Profiling is key to a successful start of any machine learning
task, and refers to the step of [thoroughly understanding our data](https://ydata.ai/resources/advanced-eda-made-simple-using-pandas-profiling): its structure, behavior, and quality.                               
In a nutshell, data profiling involves analyzing aspects related to 
the data's format and basic descriptors (e.g., number of samples,   
number/types of features, duplicate values), its intrinsic          
characteristics (such as the presence of missing data or imbalanced 
features), and other complicating factors that may arise during data
collection or processing (e.g., erroneous values or inconsistent    
features).                                                          

!!! note "Package versions"
    The integration with bytewax is available for ydata-profiling with  
    any version >=3.0.0                                                

### Simulating a streaming                                              

The below code serves to mimic a stream of data. This not require when
streaming data sources are available.

``` python linenums="1" title="Imports"
from datetime import datetime, timedelta, timezone

from bytewax.dataflow import Dataflow
from bytewax.connectors.stdio import StdOutput
from bytewax.connectors.files import CSVInput
from bytewax.testing import run_main
```

Then, we define our dataflow object. Afterwards, we will use a stateless
map method where we pass in a function to convert the string to a
datetime object and restructure the data to the format (device_id,
data). The map method will make the change to each data point in a
stateless way. The reason we have modified the shape of our data is so
that we can easily group the data in the next steps to profile data for
each device separately rather than for all the devices
simultaneously.

``` python linenums="1" title="Setup a data stream"
flow = Dataflow()
flow.input("simulated_stream", CSVInput("/content/iot_telemetry_data_1000"))

# parse timestamp
def parse_time(reading_data):
    reading_data["ts"] = datetime.fromtimestamp(float(reading_data["ts"]), timezone.utc)
    return reading_data

flow.map(parse_time)

# remap format to tuple (device_id, reading_data)
flow.map(lambda reading_data: (reading_data["device"], reading_data))
```

Now we will take advantage of the stateful capabilities of bytewax to
gather data for each device over a duration of time that we have
defined. ydata-profiling expects a snapshot of the data over time, which
makes the window operator the perfect method to use to do this.

In ydata-profiling, we are able to produce summarizing statistics for a
dataframe which is specified for a particular context. For instance, in
this example, we can produce snapshots of data referring to each IoT
device or to particular time frames:

### Profile streaming snapshots

``` python linenums="1" title="Profiling the different data snapshots"
from bytewax.window import EventClockConfig, TumblingWindow

# This is the accumulator function, and outputs a list of readings
def acc_values(acc, reading):
    acc.append(reading)
    return acc

# This function instructs the event clock on how to retrieve the
# event's datetime from the input.
def get_time(reading):
    return reading["ts"]


# Configure the `fold_window` operator to use the event time.
cc = EventClockConfig(get_time, wait_for_system_duration=timedelta(seconds=30))

# And a tumbling window
align_to = datetime(2020, 1, 1, tzinfo=timezone.utc)
wc = TumblingWindow(align_to=align_to, length=timedelta(hours=1))

flow.fold_window("running_average", cc, wc, list, acc_values)

flow.inspect(print)
```

After the snapshots are defined, leveraging ydata-profiling is as simple
as calling the ProfileReport for each of the dataframes we would like to
analyze:

``` python
import pandas as pd
from ydata_profiling import ProfileReport


def profile(device_id__readings):
    print(device_id__readings)
    device_id, readings = device_id__readings
    start_time = (
        readings[0]["ts"]
        .replace(minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )
    df = pd.DataFrame(readings)
    profile = ProfileReport(
        df, tsmode=True, sortby="ts", title=f"Sensor Readings - device: {device_id}"
    )

    profile.to_file(f"Ts_Profile_{device_id}-{start_time}.html")
    return f"device {device_id} profiled at hour {start_time}"


flow.map(profile)
```

In this example we are writing the images out to local files as part of
a function in a map method. These could be reported out via a messaging
tool, or we could save them to some remote storage in the future. Once
the profile is complete, the dataflow expects some output so we can use
the built-in [StdOutput]{.title-ref} to print the device that was
profiled and the time it was profiled at that was passed out of the
profile function in the map step:

``` python linenums="1"
flow.output("out", StdOutput())
```

There are multiple ways to execute Bytewax dataflows. In this example,
we use the same local machine, but Bytewax can also run on multiple
Python processes, across multiple hosts, in a [Docker
container](https://bytewax.io/docs/deployment/container), using a
[Kubernetes cluster](https://bytewax.io/docs/deployment/k8s-ecosystem),
and
[more](https://bytewax.io/docs/getting-started/execution#multiple-workers-manual-cluster).
In this example, we\'ll continue with a local setup, but we encourage
you to check [waxctl](https://bytewax.io/docs/deployment/waxctl) which
manages Kubernetes dataflow deployments once your pipeline is ready to
transition to production.

Assuming we are in the same directory as the file with the dataflow
definition, we can run it using:

``` linenums="1"
python -m bytewax.run ydata-profiling-streaming:flow
```

We can then use the profiling reports to validate the data quality,
check for changes in schemas or data formats, and compare the data
characteristics between different devices or time windows.

We can further leverage the [comparison report
functionality](https://ydata-profiling.ydata.ai/docs/master/pages/use_cases/comparing_datasets.html)
that highlights the differences between two data profiles in a
straightforward manner, making it easier for us to detect important
patterns that need to be investigated or issues that have to be
addressed:

``` python linenums="1" linenums="1" title="Comparing different streams"
#Generate the profile for each stream
snapshot_a_report = ProfileReport(df_a, title="Snapshot A")
snapshot_b_report = ProfileReport(df_b, title="Snapshot B")

#Compare the generated profiles
comparison_report = snapshot_a_report.compare(snapshot_b_report)
comparison_report.to_file("comparison_report.html")
```

Now you're all set to start exploring your data streams! Bytewax takes
care of all the processes necessary to handle and structure data streams
into snapshots, which can then be summarized and compared with
ydata-profiling through a comprehensive report of data characteristics.