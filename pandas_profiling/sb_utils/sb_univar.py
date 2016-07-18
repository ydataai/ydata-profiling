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

def sb_cutz(x, bins=3):
    return pd.cut(x.rank(method='min', pct=True), bins=[0, .333, .666, 1])

def plot_confusion_matrix(cm, y, title='Univariate RF Confusion matrix', cmap=plt.cm.Blues):
    plot = plt.figure(figsize=(6, 4))
    plot.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1, wspace=0, hspace=0)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(set(y)))
    plt.xticks(tick_marks)
    plt.yticks(tick_marks)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return plot


def mdl_1d(x, y):
    if x.nunique() > 10 and com.is_numeric_dtype(x):
        x = sb_cutz(x)

    series = pd.get_dummies(x)
    lr = LogisticRegressionCV(scoring='roc_auc')

    lr.fit(series, y)
    preds = lr.predict(series)

    cm = confusion_matrix(y, preds)
    plot = plot_confusion_matrix(cm, y)
    imgdata = BytesIO()
    plot.savefig(imgdata)
    imgdata.seek(0)

    aucz = lr.score(series, y)
    cmatrix = 'data:image/png;base64,' + quote(base64.b64encode(imgdata.getvalue()))
    plt.close()
    return aucz, cmatrix

