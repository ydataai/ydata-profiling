============================================
Accessing the values of correlation matrices
============================================

In some cases, directly accessing the values underneath the default visualizations provided in the report (like correlation matrices) may be useful - to generate a highly custom visualization, to reuse the computations, to do more follow-up computations, to directly change the values according to some domain-specific logic. This is possible by exploring the deeper structure of the ``ProfileReport`` object. 

The snippet below shows how to list the available correlation matrices: 

.. code-block:: python
  :caption: Listing available correlation information in the report

    # Computing the report
    data = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    profile = ProfileReport(data, title="Titanic")

    # Listing available correlation
    correlations = profile.description_set["correlations"]
    print(correlations.keys())

In this case, all the 6 possible correlation metrics were computed and the output would be ``dict_keys(['auto', 'spearman', 'pearson', 'kendall', 'cramers', 'phi_k'])``. Each ``correlations[CORRELATION_TYPE]`` object is a pandas ``DataFrame``. To access its values:

.. code-block:: python
  :caption: Accessing the values of the Pearson correlation

    # DataFrame where row and column names are the names of the original columns
    pearson_df = correlations["pearson"]

    # Actual correlation values
    pearson_mat = pearson_df.values
    print(pearson_mat)

Additional information is available on this `StackOverflow answer <https://stackoverflow.com/questions/64621116/how-can-i-get-the-numbers-for-the-correlation-matrix-from-pandas-profiling>`_. 