import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.cross_validation import train_test_split
from pandas.core import common as com

try:
    from StringIO import BytesIO
except ImportError:
    from io import BytesIO

try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote

import base64

import matplotlib
from matplotlib import pyplot as plt
from IPython.core.debugger import Tracer


def sb_cutz(x, bins=10):
    return pd.cut(x.rank(method='min', pct=True), bins=np.linspace(0, 1, bins + 1))


def plot_confusion_matrix(cm, y, title='Univariate Confusion Matrix', cmap=plt.cm.Blues):
    plot = plt.figure(figsize=(6, 4))
    #plot.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(set(y)))
    plt.xticks(tick_marks)
    plt.yticks(tick_marks)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    ax = plt.gca()
    ax.grid(False, which="majorminor")
    return plot


def mdl_1d(x, y):
    """builds univariate model to calculate AUC"""
    if x.nunique() > 10 and com.is_numeric_dtype(x):
        x = sb_cutz(x)

    series = pd.get_dummies(x, dummy_na=True)
    lr = LogisticRegressionCV(scoring='roc_auc')

    lr.fit(series, y)
    try:
        preds = (lr.predict_proba(series)[:, -1])
        #preds = (preds > preds.mean()).astype(int)
    except ValueError:
        Tracer()()

    try:
        cm = confusion_matrix(y, (preds > y.mean()).astype(int))
    except ValueError:
        Tracer()()

    plot = plot_confusion_matrix(cm, y)

    imgdata = BytesIO()
    plot.savefig(imgdata)
    imgdata.seek(0)

    aucz = roc_auc_score(y, preds)
    cmatrix = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close()
    return aucz, cmatrix




def plot_cat(series,y,title="Categorical Plot"):
    y2=pd.Series(y)
    tab = pd.concat([y2.groupby(series).count(),y2.groupby(series).mean()],axis=1)
    tab.reset_index(inplace=True)
    tab.columns = ['Value','Count','Mean(y)']
    fign = plt.figure(figsize=(6, 4))
    ax1 = fign.add_subplot(111)
    ax1.bar(tab.index,tab['Count'],.5,color='b',align='center')
    ax2 = ax1.twinx()
    ax2.plot(tab.index,tab['Mean(y)'],'-r',linewidth=4)
    plt.title(title)
    #ax1.set_xlabel('Value')
    ax1.set_xticks(tab.index)
    ax1.set_xticklabels(tab['Value'], rotation=40, ha='right')
    ax1.set_ylabel('Number of Observations',color='b')
    ax2.set_ylabel('Mean(y)', color='r')
    for t1 in ax1.get_yticklabels():
        t1.set_color('b')  
    for t2 in ax2.get_yticklabels():
        t2.set_color('r')  
    plt.tight_layout()
    return fign


def mdl_1d_cat(x, y):
    """builds univariate model to calculate AUC"""
    if x.nunique() > 10 and com.is_numeric_dtype(x):
        x = sb_cutz(x)

    series = pd.get_dummies(x, dummy_na=True)
    lr = LogisticRegressionCV(scoring='roc_auc')

    lr.fit(series, y)
    try:
        preds = (lr.predict_proba(series)[:, -1])
        #preds = (preds > preds.mean()).astype(int)
    except ValueError:
        print "preds error"
        Tracer()()

    plot = plot_cat(x, y)

    imgdata = BytesIO()
    plot.savefig(imgdata)
    imgdata.seek(0)

    aucz = roc_auc_score(y, preds)
    cmatrix = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close()
    #print aucz, plot, cmatrix
    return aucz, cmatrix