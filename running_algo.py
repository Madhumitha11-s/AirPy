import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from running_algo import *
import pandas as pd
from group_functions import *
from sub_super_script import *
from html_utils import *
from std_mean_ratio_method import *
from range_method import *
from formatting import *
from init_html import *
from get_unit_check import *
from plot_diurnal import *
from numbers_to_strings import *


def clean_MAD_outlier_running(df_temp,local_df, col):
    true_df = local_df.copy(deep=True)
    df_nan = df_temp[df_temp[col+'_clean'].notna()]
    import copy
    seq = df_nan[col+'_clean'].to_numpy()
    seq2 = copy.deepcopy(seq)
    days =1
    hours = 24*days
#     window_size = 1*4*hours
    window_size = 3
    nan_window_size = int(window_size/2)

    for i in range(len(seq) - window_size + 1):
        arr = (seq[i: i + window_size]) #getting 24 hour window

        (seq2[i: i + window_size]) = outlier_mad(arr)[0]

    df_nan = df_nan[[col, "dates"]].copy()
    df_nan[col+'_clean_outliers'] = seq2
    df_nan

    t1 = true_df.copy(deep=True)
    t1.set_index(['dates'],inplace=True)
    t2 =df_nan
    t2.set_index(['dates'],inplace=True)



    df3 = pd.concat([t1,t2],axis=1)
    df3 = df3.reset_index(drop=True)
    df3['dates'] = local_df['dates']



    return df3

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
        if (t) > threshold:
            outlier.append(arr[i])
            clean.append(np.nan)
        else:
            clean.append(arr[i])
            continue

    return clean, len(outlier)
def rolling_remove_consecutives(local_df, col):
    true_df = local_df.copy(deep=True)
    df_nan = local_df[local_df[col].notna()]
    if col == 'SO2':
        days = 7
    if col == 'Ozone':
        days = 2
    else:
        days = 1

    hours = 24*days
    window_size = 1*4*hours

    nan_window_size = int(window_size/2)
    # df_nan['temp'] =  np.where(df_nan[col] <= 1, df_nan[col] + 1 , df_nan[col])
    df_nan['temp'] =  df_nan[col] + 1
    seq = df_nan['temp'].to_numpy()
    ratio = []
    for i in range(len(seq) - window_size + 1):
        arr = (seq[i: i + window_size]) #getting 24 hour window
        t = np.nanstd(arr)/ np.nanmean(arr)
        ratio.extend([t])

    ratio = np.concatenate((np.asarray([[np.nan]*nan_window_size]), ratio), axis=None)
    len_x = len(df_nan) - len(ratio)
    ratio = np.concatenate(( ratio, np.asarray([[np.nan]*len_x]))  , axis=None)

    df = pd.DataFrame()
    df[col] = df_nan[col]
    df['dates'] = df_nan['dates']
    df["ratio"] = ratio
    df[col + '_clean']= np.where(df['ratio'] <= 0.1, np.nan, df[col])
    del df["ratio"]
    del df[col]

    t1 = local_df.copy(deep=True)
    t1.set_index(['dates'],inplace=True)
    t2 =df
    t2.set_index(['dates'],inplace=True)



    df3 = pd.concat([t1,t2],axis=1)
    df3 = df3.reset_index(drop=True)
    df3['dates'] = local_df['dates']



    return df3

def return_mean(df, col, station_name, st_no):
    return [df[col + '_clean'].mean(), df[col + '_clean_outliers'].mean(), df[col].mean(), col, station_name, st_no]

def return_count(true_df,station_name,st_no, col):
    #output of counts from copy
    list1 = [true_df[col + '_clean'].count(), true_df[col+'_clean_outliers'].count(),
             true_df[col].count(),  true_df['dates'].count(), station_name,st_no, col]
    import csv
    with open("percent_new_with_outlier.csv", "a", newline='') as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(list1)
    return

def group_plot(only_plots, local_df, col, label,station_name,st_no):

    df_temp = rolling_remove_consecutives(local_df, col)
    df_temp = find_abs_rep(df_temp, col, station_name)
    df = clean_MAD_outlier_running(df_temp,local_df, col)

    lst = [df_temp[col + '_clean'].mean(), df[col + '_clean_outliers'].mean(), df_temp[col].mean(), col, station_name, st_no]

    with open("mean_variation.csv", "a", newline='') as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(lst)

    lst = [df_temp[col + '_clean'].count(), df[col + '_clean_outliers'].count(), df_temp[col].count(),  df_temp['dates'].count(), col, station_name, st_no]

    with open("count_variation.csv", "a", newline='') as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(lst)

    #Plot the results
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=only_plots['dates'], y=only_plots[col],mode='markers',line=dict(color='red'), name='actual',marker=dict( size = 1)))
    fig.add_trace(go.Scatter(x=df_temp['dates'], y=df_temp[col+'_clean'], mode='markers',line=dict(color='black'), name='Constant values',marker=dict( size = 1)))
    fig.add_trace(go.Scatter(x=df['dates'], y=df[col+'_clean_outliers'], mode='markers',line=dict(color='blue'), name='Outlier cleaner',marker=dict( size = 1)))
    fig.update_layout(legend= {'itemsizing': 'constant'}, template = "simple_white")
    if (col == 'PM25')or(col == 'PM10') or (col == 'SO2') or (col == 'Ozone'):
        yaxis_title= str(label) + " concentration in µg/m³"
        fig.update_layout(xaxis_title="Date", yaxis_title= str(label) + " concentration in µg/m³")
    else:
        yaxis_title= str(label) + " concentration in reported units"
        fig.update_layout(xaxis_title="Date", yaxis_title= str(label) + " concentration in reported units")
    fig.update_layout(legend=dict(yanchor="top",xanchor="left"))
    fig.update_traces(mode='lines')
    fig.add_annotation(text= "Station ID: " + str(st_no),
                        align='left',
                        showarrow=False,
                        xref='paper',
                        yref='paper',
                        x=0.01,
                        y=0.95,
                        bordercolor='black',
                        borderwidth=1)
    fig.update_layout(legend= {'itemsizing': 'constant'}, template = "simple_white")
    fig.update_layout(legend=dict(yanchor="top",xanchor="left"))

    figures_to_html_app([fig], station_name+ '.html')

    true_df = local_df.copy(deep=True)
    true_df[col+'_clean'] = df_temp[col+'_clean']
    true_df[col+'_clean_outliers'] =df[col+'_clean_outliers']

    return_count(true_df, station_name,st_no, col)

    fig, ax = plt.subplots()
    df = true_df
    get_diurnal(df, col + '_clean', 'blue', 'title', ax)
    get_diurnal(df, col + '_clean_outliers', 'cyan', 'title', ax)
    get_diurnal(df, col, 'red', 'title', ax)
    plt.title(str(station_name))
    plt.xticks(np.arange(0,24, 1.0))
    plt.grid(color = '#F5F5F5')
    ax.axvspan(16, 20, alpha=0.1, color='red', label = 'Peak traffic hours')
    ax.axvspan(7, 11, alpha=0.1, color='red')
    ax.legend(loc='upper right')
    plt.xlabel("Hours")
    plt.ylabel(str(yaxis_title))

    write_html_fig(fig, station_name)


    return true_df
