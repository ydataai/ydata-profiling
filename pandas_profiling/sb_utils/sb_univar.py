import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegressionCV
from sklearn.linear_model import LassoLarsIC
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
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
    lr = LogisticRegressionCV(scoring='roc_auc')
    lars = LassoLarsIC(criterion='aic')

    if x.nunique() > 10 and com.is_numeric_dtype(x):
        x2 = sb_cutz(x)
        series = pd.get_dummies(x2, dummy_na=True)
    else:
        series = pd.get_dummies(x, dummy_na=True)

    lr.fit(series, y)
    lars.fit(series, y)

    try:
        preds = (lr.predict_proba(series)[:, -1])
        #preds = (preds > preds.mean()).astype(int)
    except ValueError:
        Tracer()()

    # try:
    #    cm = confusion_matrix(y, (preds > y.mean()).astype(int))
    # except ValueError:
    #    Tracer()()

    aucz = roc_auc_score(y, preds)

    ns = num_bin_stats(x, y)

    nplot = plot_num(ns)
    #plot = plot_confusion_matrix(cm, y)

    imgdata = BytesIO()
    nplot.savefig(imgdata)
    imgdata.seek(0)
    nplot = 'data:image/png;base64,' + \
        quote(base64.b64encode(imgdata.getvalue()))
    plt.close()

    bplot = plot_bubble(ns)
    imgdatab = BytesIO()
    bplot.savefig(imgdatab)
    imgdatab.seek(0)
    bplot = 'data:image/png;base64,' + \
        quote(base64.b64encode(imgdatab.getvalue()))
    plt.close()

    return aucz, nplot, bplot


def plot_num(numstats):
    fign = plt.figure(figsize=(9, 6))
    ax1 = fign.add_subplot(111)
    ax1.bar(numstats.index, numstats['Count'], .5, color='b', align='center')
    ax2 = ax1.twinx()
    ax2.plot(numstats.index, numstats['Target_Rate'], '-r', linewidth=4)
    plt.title("Numeric Variable Univariate View")
    ax1.set_xlabel(' bin')
    ax1.set_xticks(numstats.index)
    ax1.set_xticklabels(numstats['bin'], rotation=40, ha='right')
    ax1.set_ylabel('Number of Observations', color='b')
    ax2.set_ylabel('Target Rate', color='r')
    for t1 in ax1.get_yticklabels():
        t1.set_color('b')
    for t2 in ax2.get_yticklabels():
        t2.set_color('r')
    return fign


def plot_bubble(numstats):
    bubbles = numstats.loc[((numstats['bin'].apply(lambda x: str(x)) != 'MISS') & (
        numstats['bin'].apply(lambda x: str(x)) != 'ZERO'))].copy()
    bubbles['bubsize'] = bubbles['Count'].apply(
        lambda x: int((x / np.mean(bubbles['Count'])) * 200))
    figb = plt.figure(figsize=(9, 6))
    plt.scatter(x=bubbles['Mean'], y=bubbles['Target_Rate'],
                s=bubbles['bubsize'], c='b', label='Pop Size')
    plt.hold(True)
    plt.plot(bubbles['Mean'], bubbles['Target_Rate'],
             '-r', linewidth=4, label='Target Rate')
    plt.title("Relational Bubble Plot")
    plt.xlabel('Mean Variable')
    plt.ylabel('Target Rate', color='r')
    plt.legend()
    return figb


def num_bucket_assign(data, var, bins):

    # find all unique values (Non-Missing) and sort in ascending sequence
    temp = data[[var]].loc[data[var].notnull()].copy()

    try:
        temp['qcut_bins'] = pd.qcut(temp[var], 10)

        v = temp['qcut_bins'].unique()

        # create data frame to include bin thresholds
        b = pd.DataFrame(index=range(0, len(v)), columns=['bin'])

        for i in range(0, len(v)):
            b['bin'].iloc[i] = (min(temp[var].loc[temp['qcut_bins'] == v[i]]),
                                max(temp[var].loc[temp['qcut_bins'] == v[i]]))

        bin_cuts = b.sort_values(by='bin').reset_index(drop=True)
        # print "           - qucut worked"

    except:
        # print "           - qucut failed"
        u = temp[var].unique()

        u.sort()

        # create data frame to include unique values, counts, and assigned
        # buckets
        uni = pd.DataFrame(index=range(0, len(u)), columns=[
                           'value', 'count', 'bucket'])

        # determine witdh of bucket based on number of obs
        width = len(temp) / bins

        # initialize current bucket and bucket size count for loop
        csize = 0
        bucket = 0

        for i in range(0, len(u)):
            # get unique value and count
            uni['value'].iloc[i] = u[i]
            uni['count'].iloc[i] = len(temp.loc[temp[var] == u[i]])

            # update size for current bucket and assign bucket value
            csize = csize + uni['count'].iloc[i]
            uni['bucket'].iloc[i] = bucket

            # if current bucket size has exceeded the desired width, then start
            # next bucket
            if csize >= width:
                csize = 0
                bucket = bucket + 1

        # merge small last bins into previous bin
        if (np.sum(uni['count'][uni.bucket == max(uni['bucket'])]) < (width / 3)):
            uni['bucket'].loc[uni['bucket'] == max(
                uni['bucket'])] = max(uni['bucket']) - 1

        # create data frame to include bin thresholds
        bin_cuts = pd.DataFrame(index=range(
            0, max(uni['bucket']) + 1), columns=['bin'])

        # assign min an max bucket values
        for i in range(0, max(uni['bucket']) + 1):
            bin_cuts['bin'].iloc[i] = (min(uni.loc[uni['bucket'] == i, 'value']), max(
                uni.loc[uni['bucket'] == i, 'value']))

    # add bucket if missing values exist
    if sum(pd.isnull(data[var])) > 0:
        bin_cuts.loc[len(bin_cuts)] = 'MISS'

    # add bucket if more than 1% of non missing values are =0
    if (len(temp[var].loc[temp[var] == 0]) / float(len(temp))) > .01:
        bin_cuts.loc[len(bin_cuts)] = 'ZERO'

    return bin_cuts


def num_bin_stats(var, target, buckets=10, target_type='binary'):

    # create a temporary series to work with
    temp = pd.DataFrame()
    temp['var'] = var
    temp['target'] = target

    # create summary dataframe for output
    if target_type == 'binary':
        cutpoints = pd.DataFrame(
            columns=('bin', 'Mean', 'Count', 'N_Target', 'Miss_Target', 'Target_Rate'))
    elif target_type == 'continuous':
        cutpoints = pd.DataFrame(
            columns=('bin', 'Mean', 'Count', 'Miss_Target', 'Mean_Target'))
    else:
        raise TypeError(
            "Not a Valid Target Type (needs to be 'binary' or 'continuous')")

       # test to see if fewer levels than buckets
    if len(temp['var'].unique()) > buckets:
        granular = 1
        cutpoints['bin'] = num_bucket_assign(temp, 'var', buckets)

    else:
        granular = 0
        cutpoints['bin'] = list(temp['var'].unique())
        cutpoints['bin'].loc[cutpoints['bin'].isnull()] = 'MISS'

    for i in range(0, len(cutpoints)):
        if cutpoints['bin'][i] == 'MISS':
            temp2 = temp.loc[temp['var'].isnull()]
        elif cutpoints['bin'][i] == 'ZERO':
            temp2 = temp.loc[temp['var'] == 0]
        else:
            if granular == 1:
                temp2 = temp.loc[(temp['var'] >= cutpoints['bin'].ix[i][0]) & (
                    temp['var'] <= cutpoints['bin'].ix[i][1])]
            else:
                temp2 = temp.loc[temp['var'] == cutpoints['bin'][i]]

        cutpoints['Count'].iloc[i] = len(temp2)
        cutpoints['Mean'].iloc[i] = np.mean(temp2['var'].apply(lambda x: float(x)))
        cutpoints['Miss_Target'].iloc[i] = sum(pd.isnull(temp2['target']))

        if target_type == 'binary':
            cutpoints['N_Target'].iloc[i] = sum(temp2['target'])
            cutpoints['Target_Rate'].iloc[i] = cutpoints['N_Target'].iloc[
                i] / (float(cutpoints['Count'].iloc[i]) + 1e-9)

        if target_type == 'continuous':
            cutpoints['Mean_Target'].iloc[i] = np.mean(temp2['target'])

    cutpoints['sort'] = cutpoints['Mean']
    cutpoints['sort'].loc[cutpoints['bin'].astype(str)=='MISS'] = min(cutpoints['Mean']-2)
    cutpoints['sort'].loc[cutpoints['bin'].astype(str)=='ZERO'] = min(cutpoints['Mean']-1)
    cutpoints.sort_values('sort',inplace=True)

    return cutpoints.drop('sort',axis=1).reset_index(drop=True)


def plot_cat(series, y, title="Categorical Plot", maxn=10):
    y2 = pd.Series(y)
    tab = pd.concat([y2.groupby(series).count(),
                     y2.groupby(series).mean()], axis=1)
    tab.columns = ['Count', 'Target']
    tab.sort_values('Count', inplace=True, ascending=False)

    if len(tab) > maxn:
        short = tab[0:maxn].copy()
        short.ix['Other'] = tab[maxn:len(tab)].sum()
        tab = short.copy()

    tab.reset_index(inplace=True)
    tab.columns = ['Value', 'Count', 'Target']
    tab['Mean(y)'] = tab['Target'] / tab['Count']
    fign = plt.figure(figsize=(9, 6))
    ax1 = fign.add_subplot(111)
    ax1.bar(tab.index, tab['Count'], .5, color='b', align='center')
    ax2 = ax1.twinx()
    ax2.plot(tab.index, tab['Mean(y)'], '-r', linewidth=4)
    plt.title(title)
    ax1.set_xticks(tab.index)
    ax1.set_xticklabels(tab['Value'], rotation=40, ha='right')
    ax1.set_ylabel('Number of Observations', color='b')
    ax2.set_ylabel('Mean(y)', color='r')
    for t1 in ax1.get_yticklabels():
        t1.set_color('b')
    for t2 in ax2.get_yticklabels():
        t2.set_color('r')
    # plt.tight_layout()
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
        Tracer()()

    plot = plot_cat(x, y)

    imgdata = BytesIO()
    plot.savefig(imgdata)
    imgdata.seek(0)

    aucz = roc_auc_score(y, preds)
    cmatrix = 'data:image/png;base64,' + \
        quote(base64.b64encode(imgdata.getvalue()))
    plt.close()
    return aucz, cmatrix
