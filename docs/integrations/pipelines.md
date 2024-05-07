# Pipelines

With Python, command-line and Jupyter interfaces, `ydata-profiling`
integrates seamlessly with DAG execution tools like Airflow, Dagster,
Kedro and Prefect, allowing it to easily becomes a building block of
data ingestion and analysis pipelines. Integration with
[Dagster](https://github.com/dagster-io/dagster) or
[Prefect](https://github.com/prefecthq/prefect) can be achieved in a
similar way as with Airflow.

## YData Fabric pipelines

!!! tip "Fabric Community version"
    
    [YData Fabric](https://ydata.ai/products/fabric) has a community version that you can start using today to create data workflows with pipelines. 
    [Sign up here](http://ydata.ai/register?utm_source=ydata-profiling&utm_medium=documentation&utm_campaign=YData%20Fabric%20Community) and start building your pipelines. ydata-profiling is installed by default in all YData images.

![ydata-profiling in a pipeline](../_static/img/profiling_pipelines.png)

YData Fabric's data pipelines are engineered to harness the capabilities of [Kubeflow](https://www.kubeflow.org/), providing a robust foundation for scalable and efficient data workflows. 
This technical integration ensures that data pipelines can seamlessly handle high data volumes and execute operations with optimal resource utilization.

YData Fabric simplifies the process of data pipeline setup by abstracting complexity. 
The setup is done through a drag-and-drop experience while leveraging existing Jupyter Notebook environments. 
Check this video to see [how to create a pipeline in YData Fabric](https://www.youtube.com/watch?v=feNoXv34waM&t=8s).

```python linenums="1" title="Profile a csv with ydata-profiling in a pipeline"
# Import required packages
import json

import pandas as pd
from ydata.profiling import ProfileReport

# Read your dataset as a CSV
dataset = pd.read_csv('data.csv')

# Instantiate the report
report = ProfileReport(dataset, title="Profiling my data")
report.config.html.navbar_show = False #disable the navigation bar


# get the report html
report_html = report.to_html()

#Output visually in the pipeline
metadata = {
    'outputs' : [
        {
      'type': 'web-app',
      'storage': 'inline',
      'source': report_html,
    }
    ]
  }

#write the visual outputs in the pipeline flow
with open('mlpipeline-ui-metadata.json', 'w') as metadata_file:
    json.dump(metadata, metadata_file)
```

You can find the notebook with this implementation in [ydata-profiling examples folder](https://github.com/ydataai/ydata-profiling/blob/develop/examples/integrations/ydata_fabric_pipelines/data_profiling.ipynb). 

## Airflow

Integration with Airflow can be easily achieved through the
[BashOperator](https://airflow.apache.org/docs/stable/_api/airflow/operators/bash_operator/index.html)
or the
[PythonOperator](https://airflow.apache.org/docs/stable/_api/airflow/operators/python_operator/index.html#airflow.operators.python_operator.PythonOperator).

``` python linenums="1" title="ydata-profiling with Airflow"
# Using the command line interface
profiling_task = BashOperator(
    task_id="Profile Data",
    bash_command="pandas_profiling dataset.csv report.html",
    dag=dag,
)
```

``` python linenums="1" title="ydata-profiling with Airflow"
# Using the Python interface
import ydata_profiling

def profile_data(file_name, report_file):
    df = pd.read_csv(file_name)
    report = pandas_profiling.ProfileReport(df, title="Profiling Report in Airflow")
    report.to_file(report_file)

    return "Report generated at {}".format(report_file)


profiling_task2 = PythonOperator(
    task_id="Profile Data",
    op_kwargs={"file_name": "dataset.csv", "report_file": "report.html"},
    python_callable=profile_data,
    dag=dag,
)
```

## Kedro

There is a community created [Kedro
plugin](https://github.com/BrickFrog/kedro-pandas-profiling) available.

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=2d9fcb48-0fa6-43d8-a0ba-fdad344050fd" />