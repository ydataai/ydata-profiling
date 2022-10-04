# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# heading
st.write("""
# **Exploratory Data Analysis (EDA)**
""")

with st.sidebar.header("Upload you dataset (.csv)"):
    uploaded_file = st.sidebar.file_uploader('Upload your file', type=['csv'])
    df = sns.load_dataset('titanic')
    
Machine_Learning_Model_name = st.sidebar.selectbox('Select Model', (
    'Linear R', 'Decision tree R', 'KNN R', 'SVR R'))

    # profiling report for pandas

if uploaded_file is not None:
    #@st.cache
    def load_data():
        csv = pd.read_csv(uploaded_file, encoding='latin-1')
        return csv
    df = load_data()
    st.header("EDA")
    st.header("Shape")
    row, col = df.shape

    st.write(df.shape)
    st.write("Number of Rows:", row)
    st.write("Number of Columns:", col)
    st.header("Structure of table")
    st.write(df.info())
    st.write("Find Missing Values", df.isnull().sum())
    st.write("Percentage Calculation of Missing Values",
             df.isnull().sum() / df.shape[0] * 100)
    st.write("Columns:", df.columns)
    df.dropna(inplace=True)
    st.write("After dropping columns cotaining 90% null values", df)
    st.write("Summary Statistics", df.describe())
    st.write("Value Count of a Specific Column",
             df.iloc[:, 1].value_counts())
    st.write("Standard Normal Distribution", sns.histplot(df.iloc[:, 1]))
    st.write("Measure its Skewness and Kurtosis of a Specific Column",
             df.iloc[:, 4].agg(['skew', 'kurtosis']).transpose())
    corr = df.corr(method="pearson")
    st.write("Correlation", corr)
    if st.checkbox("Show code"):
        with st.echo():
            st.write("Code")
            #fig =px.violin(x=df["price_range"], y=df["ram"],color=df["n_cores"], box=True # draw box plot inside the violin
            #)
            #st.write("Violin plot",fig.update_layout(width=800, height=400))
            #fig = px.histogram(df, x="mobile_wt", y="fc", color="price_range",marginal="box",hover_data=df.columns)
            #st.write("Hist plot",fig.update_layout(width=800, height=400))

    fig = px.violin(x=df["price_range"], y=df["ram"],color=df["n_cores"], box=True # draw box plot inside the violin
               )
    st.write("Violin plot",
             fig.update_layout(width=800, height=400)
             )
    fig = px.histogram(df, x="mobile_wt", y="fc", color="price_range",
                   marginal="box",
                   hover_data=df.columns)
    st.write("Hist plot",
             fig.update_layout(width=800, height=400))
    fig = px.scatter(df, x='battery_power', y='ram', size='n_cores', color='price_range', hover_name='price_range',
                     log_x=True, animation_frame='battery_power', animation_group='price_range',range_x=[1, 2000], range_y=[1, 4000])
    
    st.write("Scattar plot",
             fig.update_layout(width=800, height=400)
             )
else:
        st.info('Awaiting for CSV file, upload kar b do ab ya kam nh lena?')
        if st.button('Press to use example data'):
            @st.cache
            def load_data():
                a = pd.DataFrame(np.random.rand(100, 5), columns=[
                                 'Age', 'Banana', 'Codanics', 'Duetchland', 'Ear'])
                return a
            df = load_data()
            pr = ProfileReport(df, explorative=True)
            st.header("**Input DF**")
            st.write(df)
            st.write('---')
            st.header('**Profiling report with pandas**')
            st_profile_report(pr)


def get_dataset(uploaded_file):
    x = df.iloc[:, 4:13]
    y = df.iloc[:, -1]
    return x, y


X, y = get_dataset(uploaded_file)









# Regression
# CLassification

# Machine Learning models
def add_parameter_ui(Machine_Learning_Model_name):
    params = dict() # create an empty dictionary

    if Machine_Learning_Model_name == 'Linear R':
        L = st.sidebar.slider('L', 1, 15)
        params['L'] = L 
    elif Machine_Learning_Model_name == 'KNN R':
        KR = st.sidebar.slider('KR', 1, 15)
        params['KR'] = KR
    elif Machine_Learning_Model_name == 'SVR R':
        S = st.sidebar.slider('S', 1, 15)
        params['S'] = S 
    else:
        max_depth = st.sidebar.slider('max_depth', 2, 15)
        params['max_depth'] = max_depth
        n_estimators = st.sidebar.slider('n_estimators', 1, 100)
        params['n_estimators'] = n_estimators  # number of trees
    return params

# calling function
params = add_parameter_ui(Machine_Learning_Model_name)

# Model running
def get_model(Machine_Learning_Model_name,params):
    clf = None
    if Machine_Learning_Model_name == 'Linear R':
        clf = LinearRegression()
    elif Machine_Learning_Model_name == 'KNN R':
        clf = KNeighborsRegressor()
    elif Machine_Learning_Model_name == 'SVR R':
        clf = SVR()
    else:
            clf = clf = DecisionTreeRegressor(random_state=1234)
    return clf


# calling function
clf = get_model(Machine_Learning_Model_name, params)

# Training and testing model
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=1234)

# Fitting and predicting model
clf.fit(X_train,y_train)
y_pred= clf.predict(X_test)

# Model Accuracy
#acc=clf.score(X_test, y_test)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
st.write(f'Model = {Machine_Learning_Model_name}')
#st.write(f'Accuracy = {acc}')
st.write(f'R2 = {r2}')
st.write(f'Mean Absolute Error = {mae}')
st.write(f'Mean Squared Error = {mse}')





#### PLOT DATSET ####
# ab hum apnay sary sary features ka 2 dimentional plot pay draw kr dayn gay using pca
pca = PCA(2)
X_projected = pca.fit_transform(X)

# ab hum apna data 0 or 1 dimension may slice kr dayn gay
x1 = X_projected[:, 0]
x2 = X_projected[:, 1]

fig = plt.figure()
plt.scatter(x1, x2, c=y, alpha=0.8, cmap='viridis')

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar()

# plt.show()
st.pyplot(fig)

