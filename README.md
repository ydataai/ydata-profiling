#pandas-profiling 
Generates profile reports from a pandas DataFrame. The df.describe() function is great but a little basic for serious exploratory data analysis. 

For each column the following statistics - if relevant for the column type - are presented in a nice interactive HTML report:

* ** Essentials**:  type, unique values (# and %), missing values (# and %)
* ** Quantile statistics** like minimum value, Q1, median, Q3, maximum, range, interquartile range
* **Descriptive statistics **like mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness
* **Most frequent values**
* **Histogram**


## Demo

Here is a demo of a report that has been generated

## Usage
The profile report is written in HTML5 and CSS3, which means pandas-profiling requires a modern browser. 

### Jupyter Notebook (formerly IPython)
We recommend generating reports interactively by using the Jupyter notebook. 

With a DataFrame df defined as follows:

	import pandas as pd
	

	


### Command line
You can also use the command line interface to generate a report file on your local disk from a CSV file and subsequently open it.

## Dependencies

* **An internet connection.** Pandas-profiling requires an internet connection to download the Bootstrap and JQuery libraries. I might change this in the future, let me know if you want that sooner than later.
* pandas
* matplotlib


