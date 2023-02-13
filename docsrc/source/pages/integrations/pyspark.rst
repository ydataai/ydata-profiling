============
⚡ Pyspark
============

.. NOTE::
   **Spark dataframes support**
    - Spark Dataframes profiling is available from ydata-profiling version 4.0.0 onwards

Data Profiling is a core step in the process of developing AI solutions.
For small datasets, the data can be loaded into memory and easily accessed with Python and pandas dataframes.
However for larger datasets what can be done?

Big data engines, that distribute the workload through different machines, are the answer.
Particularly, Spark rose as one of the most used and adopted engines by the data community.
``ydata-profiling`` provides an ease-to-use interface to generate complete and comprehensive
data profiling out of your Spark dataframes with a single line of code.

Getting started
---------

+++++++++++++++
Installing Pyspark for Linux and Windows
+++++++++++++++

* Ensure that you first install the system requirements (spark and java).
    - Go to `Download Java JDK <https://www.oracle.com/java/technologies/javase-jdk13-downloads.html>`_ and download the Java Development Kit (JDK).
    - Download and install a `Spark version bigger than 3.3 <https://spark.apache.org/downloads.html>`_
* Set your environment variables

.. code-block:: console
    export SPARK_VERSION=3.3.0
    export SPARK_DIRECTORY=/opt/spark
    export HADOOP_VERSION=2.7

    mkdir -p ${SPARK_DIRECTORY}
    sudo apt-get update
    sudo apt-get -y install openjdk-8-jdk
    curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    --output ${SPARK_DIRECTORY}/spark.tgz
    cd ${SPARK_DIRECTORY} && tar -xvzf spark.tgz && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} sparkenv
A more detailed tutorial for the installation can be found `here <https://www.datacamp.com/tutorial/installation-of-pyspark>`__.

+++++++++++++++
Installing Pyspark for MacOS
+++++++++++++++

* Use `Homebrew` to ensure that the system requirements are installed (java and scala (optional))
.. code-block:: console
    brew install openjdk@11

.. code-block:: console
    #Install scala is optional
    brew install scala
* Install pyspark
.. code-block:: console
    brew install apache-spark

After successful installation of Apache Spark run pyspark from the command line to launch PySpark shell and confirm both python and pyspark versions.
A more detailed tutorial for the installation can be found `here <https://sparkbyexamples.com/pyspark/how-to-install-pyspark-on-mac/>`__

+++++++++++++++
Install ydata-profiling
+++++++++++++++

* Create a pip virtual environment or a conda environment and install ``ydata-profiling`` with pyspark as a dependency

.. code-block::
    pip install ydata-profiling[pyspark]

Profiling with Spark DataFrames
-------------------------------

A quickstart example to profile data from a CSV leveraging Pyspark engine and ``ydata-profiling``.

.. code-block::
    from pyspark.sql import SparkSession

    spark = SparkSession.builder().master("local[1]")
          .appName("SparkByExamples.com")
          .getOrCreate()

    df = spark.read.csv("{insert-file-path}")

    df.printSchema()

    a = ProfileReport(df)
    a.to_file("spark_profile.html")

ydata-profiling in Databricks
---------

Yes! We have fantastic new coming with a full tutorial on how you can use ydata-profiling in Databricks Notebooks.

The notebook example can be found `here <https://github.com/ydataai/ydata-profiling/tree/master/examples/integrations/databricks_example.ipynb>`_.

Stay tuned - we are going to update the documentation soon!