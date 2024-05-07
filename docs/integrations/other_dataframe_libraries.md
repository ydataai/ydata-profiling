# Other DataFrame libraries

`ydata-profiling` is built on `pandas` and `numpy`. Pandas supports a
wide range of data formats including CSV, XLSX, SQL, JSON, HDF5, SAS,
BigQuery and Stata. Read more on [supported formats by
Pandas](https://pandas.pydata.org/docs/user_guide/io.html).

If you have data in another framework of the Python Data ecosystem, you
can use `ydata-profiling` by converting to a pandas `DataFrame`, as
direct integrations are not yet supported. Large datasets might require
sampling (as seen in our documentation on [how to profile large datasets](../features/big_data.md)).

```python linenums="1" title="Dask to Pandas"
# Convert dask DataFrame to a pandas DataFrame
df = df.compute()
```

```python linenums="1" title="Vaex to Pandas"
# Convert vaex DataFrame to a pandas DataFrame
df = df.to_pandas_df()
```
!!! note "Modin interface"

    This is not part of the API as pandas.DataFrame, naturally, does not posses such a method.
    You can use the private method DataFrame._to_pandas() to do this conversion.
    If you would like to do this through the official API you can always save the Modin DataFrame to
    storage (csv, hdf, sql, ect) and then read it back using Pandas. This will probably be the safer
    way when working big DataFrames, to avoid out of memory issues."
    Source: https://github.com/modin-project/modin/issues/896

```python linenums="1" title="Modin to Pandas"
# Convert modin DataFrame to pandas DataFrame
df = df._to_pandas()
```

<img referrerpolicy="no-referrer-when-downgrade" src="https://static.scarf.sh/a.png?x-pxid=baa0e45f-0c03-4190-9646-9d8ea2640ba2" />