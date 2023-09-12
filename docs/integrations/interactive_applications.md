# Interactive applications

The `ydata-profiling` report, through several of its interfaces, can be
integrated in interactive data applications such as those developed with
[Streamlit](https://streamlit.io) or [Panel](https://panel.holoviz.org).

## Streamlit

[Streamlit](https://www.streamlit.io) is an open-source Python library
made to build web-apps for machine learning and data science.

!!! note

    This feature is only available for versions previous to ydata-profiling
    (<=3.6.2).

![image](https://user-images.githubusercontent.com/9756388/140196751-69b0a361-99ed-4fc3-8282-cb0cd1fb0d59.gif)

``` python linenums="1" title="Creating a simple Streamlit app with ydata-profiling"
import pandas as pd
import ydata_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report
df = pd.read_csv(
    "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
)
pr = df.profile_report()

st.title("Profiling in Streamlit")
st.write(df)
st_profile_report(pr)
```

You can install the [ydata-profiling
component](https://github.com/Ghasel/streamlit-pandas-profiling) for
Streamlit with pip.

``` console
pip install streamlit-pandas-profiling
```

## Dash

[Dash](hhttps://github.com/plotly/dash) is a Python framework for
building machine learning & data science web apps, built on top of
Plotly.js, React and Flask. It is commonly used for interactive data
exploration, precisely where `ydata-profiling` also focuses. Inline
access to the insights provided by `ydata-profiling` can help guide the
exploratory work allowed by Dash. To integrate a Profiling Report inside
a Dash app, two options exist:

### Load HTML version of report as an asset

Assuming the HTML version of the report is in `report.html`, move it to
a folder called `assets`. The snippet below shows a simple Dash app,
`app.py`, embedding this report:

``` python linenums="1" title="Create a Dash dashboard with ydata-profiling integrated"
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
```

When running `python app.py`, a Dash app with the report embedded will
be available on <http://127.0.0.1:8050>.

### Directly embed the raw HTML

A more unorthodox option requiring no explicit file handling involves
using the `dash-dangerously-set-inner-html` library to directly embed
the HTML raw text (thus requiring no HTML export). Install the library
through `pip`:

``` console
pip install dash-dangerously-set-inner-html
```

And configure the Dash app as in the following snippet:

``` python linenums="1" title="Embed the raw html into Dash"
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
```

When running `python app.py`, a Dash app with the report embedded will
be available on
`` <http://127.0.0.1:8050>`_. While this option is somewhat more direct, **the embedded report will not be fully interactive, with some buttons unclickable**.    Panel -----  For more information on how to use ``ydata-profiling\`[
in Panel, see \`this GitHub issue
\<https://github.com/ydataai/ydata-profiling/issues/491\>]{.title-ref}\_
and [this integration
example](https://awesome-panel.org/pandas_profiling_app).
