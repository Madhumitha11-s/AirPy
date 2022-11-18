
import csv
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt

import calendar
import warnings
import pickle
import glob
from datetime import datetime, timedelta
import os
import plotly.express as px

import base64
from io import BytesIO
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import csv
import seaborn as sns
from scipy import stats

from group_functions import *
from sub_super_script import *
from html_utils import *
from std_mean_ratio_method import *
from range_method import *
from so2_cleaner import *

def outlier_mad(arr):
    """
    Here arr is the 24 hour window values

    """
    med = np.nanmedian(arr, axis = 0)
    mad = np.nanmedian(np.absolute(arr - np.nanmedian(arr)))
    threshold = 3.5
    outlier = []
    clean = []
    index=0

    for i, v in enumerate(arr):
        t = (v-med)/mad
        if t > threshold:
            outlier.append(arr[i])
            clean.append(np.nan)
        else:
            clean.append(arr[i])
            continue

    return clean, len(outlier)


def interpolate_gaps(values, limit=None):
    """
    Fill gaps using linear interpolation, optionally only fill gaps up to a
    size of `limit`.
    """
    values = np.asarray(values)
    i = np.arange(values.size)
    valid = np.isfinite(values)
    filled = np.interp(i, i[valid], values[valid])

    if limit is not None:
        invalid = ~valid
        for n in range(1, limit+1):
            invalid[:-n] &= invalid[n:]
        filled[invalid] = np.nan

    return filled


def interpolate_gaps(values, limit=None):
    """
    Fill gaps using linear interpolation, optionally only fill gaps up to a
    size of `limit`.
    """
    values = np.asarray(values)
    i = np.arange(values.size)
    valid = np.isfinite(values)
    filled = np.interp(i, i[valid], values[valid])

    if limit is not None:
        invalid = ~valid
        for n in range(1, limit+1):
            invalid[:-n] &= invalid[n:]
        filled[invalid] = np.nan

    return filled


def find_abs_rep(local_df, col, station_name):
    unchanged = local_df.copy(deep = True)

    ar1 = interpolate_gaps(local_df[col].to_numpy(), limit=2)
    local_df[col + '_ab_rep'] = ar1
    values_repeats = []
    count_repeats = []
    starttime = []
    endtime = []
    for k, v in local_df.groupby((local_df[col + '_ab_rep'].shift() != local_df[col + '_ab_rep']).cumsum()):
        if (len(v[col + '_ab_rep']) >= 12) == True:
            values_repeats.append(v[col].iloc[-1].item())
            count_repeats.append(len(v[col + '_ab_rep']))
            starttime.append(v['dates'].iloc[0])
            endtime.append(v['dates'].iloc[-1])
            local_df['hint'] = local_df.dates.between((v['dates'].iloc[0]), (v['dates'].iloc[-1]))
            local_df[col + '_ab_rep'] = np.where(local_df['hint'] == True, np.nan, local_df[col + '_ab_rep'])

    temp = pd.DataFrame(
        {'values_repeats': values_repeats,
         'count_repeats': count_repeats,
         'starttime':starttime ,
         "endtime": endtime,
         "pol_name": col,
         'station_name': station_name
        })
    temp.to_csv('absolute_repeats.csv', mode='a', index=False, header=False)
    unchanged[col + '_ab_rep'] = local_df[col + '_ab_rep']
    return unchanged

def get_clean_by_diff(local_df, col,col_name,station_name,st_no, t, cutoff):

    unchanged = local_df.copy(deep = True)
    # import pdb; pdb.set_trace()



    ar1 = interpolate_gaps(local_df[col].to_numpy(), limit=2)
    ar1 = np.diff(ar1)
    ar1 = np.abs(np.append(ar1, 0))
    local_df[col + '_label_diff'] = ar1
    local_df[col + '_label_diff']= np.where(local_df[col + '_label_diff'] <= 1, 0, local_df[col + '_label_diff'])
    local_df[col + '_clean'] = local_df[col]
    local_df[col + '_diff'] = ar1


    values_repeats = []
    count_repeats = []
    starttime = []
    endtime = []


    for k, v in local_df.groupby((local_df[col + '_label_diff'].shift() != local_df[col + '_label_diff']).cumsum()):

        values_repeats.append(v[col].iloc[-1].item())
        count_repeats.append(len(v[col + '_label_diff']))
        starttime.append(v['dates'].iloc[0])
        endtime.append(v['dates'].iloc[-1])
        RANGE = np.max(v[col]) - np.min(v[col])
        if (len(v[col + '_label_diff']) >= 12) == True & (RANGE <= 2) == True:

            local_df['hint'] = local_df.dates.between((v['dates'].iloc[0]), (v['dates'].iloc[-1]))
            local_df[col + '_clean'] = np.where(local_df['hint'] == True, np.nan, local_df[col + '_clean'])

    df1 = rep24(local_df, col)
    local_df[col+'24hr'] = df1[col+'24hr']
    local_df[col+'_std_mean'] = df1['std_mean']

    unchanged[col+'24hr'] = local_df[col+'24hr']
    unchanged[col + '_clean'] = local_df[col + '_clean']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col],opacity=1,marker=dict(color = 'red', size = 3.5),
                        mode='markers', name='actual'))

    fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col + '_clean'],opacity=1,marker=dict(color = 'blue', size = 3.5),
                        mode='markers', name='Difference method (3h window)'))

    fig.add_trace(go.Scatter(x=local_df['dates'], y=df1[col+'24hr'],opacity=1,marker=dict(color = 'green', size = 3.5),
                        mode='markers', name='STD/MEAN method (24h window)'))

    local_df[col + '_clean_c'] = local_df[col + '_clean']
    local_df[col + '_clean_c'] = np.where((local_df[col + '_clean_c'].isnull() == False) & (df1[col+'24hr'].isnull() == True), np.nan, local_df[col + '_clean_c'])


    try:
        # import pdb; pdb.set_trace()
        local_df = find_abs_rep(local_df, col, station_name)
        local_df[col + '_clean_c'] = np.where((local_df[col + '_clean_c'].isnull() == False) & ( local_df[col + '_ab_rep'].isnull() == True), np.nan, local_df[col + '_clean_c'])
        fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col + '_clean_c'],opacity=1,marker=dict(color = 'darkblue', size = 3.5),
                            mode='markers', name='Clean Data'))
    except:
        print("error in executing ab finder")
        pass


    unchanged[col + '_clean_c'] = local_df[col + '_clean_c']


    # if (col == 'SO2'):
    #     local_df = get_threshold_so2(local_df)
    #     fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col+'_cleaned_3days'],opacity=1,marker=dict(color = 'violet', size = 3.5),
    #                         mode='markers', name='STD/MEAN method (3Days window)'))

    fig.update_layout(legend= {'itemsizing': 'constant'}, template = "simple_white")
    fig.update_layout(xaxis_title="Date", yaxis_title= str(col_name) + " concentration in µg/m³")
    fig.update_layout(legend=dict(yanchor="top",xanchor="left"))
    fig.update_traces(mode='lines')
    figures_to_html_app([fig], station_name+ '.html')

    list1 = [unchanged[col + '_clean_c'].count(), unchanged[col+'24hr'].count(), unchanged[col + '_clean'].count(), unchanged[col].count(),  unchanged['dates'].count(), station_name,st_no, col]


    with open("percent.csv", "a", newline='') as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(list1)



    return unchanged
