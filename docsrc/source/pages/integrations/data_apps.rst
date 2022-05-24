========================
Interactive applications
========================

The ``pandas-profiling`` report, through several of its interfaces, can be integrated in interactive data applications such as those developed with `Streamlit <https://streamlit.io>`_ or `Panel <https://panel.holoviz.org>`_.

Streamlit
---------

`Streamlit <https://www.streamlit.io>`_ is an open-source Python library made to build web-apps for machine learning and data science.

.. image:: https://user-images.githubusercontent.com/9756388/140196751-69b0a361-99ed-4fc3-8282-cb0cd1fb0d59.gif

.. code-block:: python

  import pandas as pd
  import pandas_profiling
  import streamlit as st
  from streamlit_pandas_profiling import st_profile_report

  df = pd.read_csv(
      "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
  )
  pr = df.profile_report()

  st.title("Pandas Profiling in Streamlit")
  st.write(df)
  st_profile_report(pr)

You can install the `pandas-profiling component <https://github.com/Ghasel/streamlit-pandas-profiling>`_ for Streamlit with pip:

.. code-block:: console

  pip install streamlit-pandas-profiling


Panel
-----

For more information on how to use ``pandas-profiling`` in Panel, see `this GitHub issue <https://github.com/pandas-profiling/pandas-profiling/issues/491>`_ and `this integration example <https://awesome-panel.org/pandas_profiling_app>`_.