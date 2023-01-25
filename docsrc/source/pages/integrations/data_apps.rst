========================
Interactive applications
========================

The ``pandas-profiling`` report, through several of its interfaces, can be integrated in interactive data applications such as those developed with `Streamlit <https://streamlit.io>`_ or `Panel <https://panel.holoviz.org>`_.

Streamlit
---------

`Streamlit <https://www.streamlit.io>`_ is an open-source Python library made to build web-apps for machine learning and data science.

.. NOTE::
    This feature is only available for versions previous to ydata-profiling (<=3.6.2).

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

  st.title("Profiling in Streamlit")
  st.write(df)
  st_profile_report(pr)

You can install the `pandas-profiling component <https://github.com/Ghasel/streamlit-pandas-profiling>`_ for Streamlit with pip:

.. code-block:: console

  pip install streamlit-pandas-profiling


Dash
----

`Dash <hhttps://github.com/plotly/dash>`_ is a Python framework for building machine learning & data science web apps, built on top of Plotly.js, React and Flask. It is commonly used for interactive data exploration, precisely where ``ydata-profiling`` also focuses. Inline access to the insights provided by ``pandas-profiling`` can help guide the exploratory work allowed by Dash. To integrate a Profiling Report inside a Dash app, two options exist:

Load HTML version of report as an asset 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming the HTML version of the report is in ``report.html``, move it to a folder called ``assets``. The snippet below shows a simple Dash app, ``app.py``, embedding this report:

.. code-block:: python

    import dash
    from dash import html

    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Iframe(
                src="assets/census_report.html",  # must be under assets/ to be properly served
                style={"height": "1080px", "width": "100%"},
            )
        ]
    )

    if __name__ == "__main__":
        app.run_server(debug=True)

When running ``python app.py``, a Dash app with the report embedded will be available on `<http://127.0.0.1:8050>`_.

Directly embed the raw HTML
^^^^^^^^^^^^^^^^^^^^^^^^^^^

A more unorthodox option requiring no explicit file handling involves using the ``dash-dangerously-set-inner-html`` library to directly embed the HTML raw text (thus requiring no HTML export). Install the library through ``pip``: 

.. code-block:: console

    pip install dash-dangerously-set-inner-html


And configure the Dash app as in the following snippet:

.. code-block:: python

    import pandas as pd
    from ydata_profiling import ProfileReport
    import dash
    from dash import html
    import dash_dangerously_set_inner_html

    # Creating the Report
    df = pd.read_csv(
        "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    )
    profile = ProfileReport(df, title="Titanic Dataset")
    text_raw = profile.to_html()

    # Creating the Dash app

    app = dash.Dash(__name__)

    app.layout = html.Div(
        [dash_dangerously_set_inner_html.DangerouslySetInnerHTML(text_raw)]
    )

    app.layout = html.Div(
        [dash_dangerously_set_inner_html.DangerouslySetInnerHTML(text_raw)]
    )

    if __name__ == "__main__":
        app.run_server(debug=True)

When running ``python app.py``, a Dash app with the report embedded will be available on ``<http://127.0.0.1:8050>`_. While this option is somewhat more direct, **the embedded report will not be fully interactive, with some buttons unclickable**.



Panel
-----

For more information on how to use ``ydata-profiling`` in Panel, see `this GitHub issue <https://github.com/ydataai/ydata-profiling/issues/491>`_ and `this integration example <https://awesome-panel.org/pandas_profiling_app>`_.