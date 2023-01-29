import pandas as pd
import numpy as np
import plotly.graph_objs as go
from html_utils import *
from plot_diurnal import *
import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.pyplot as plt

def convert_to_micro(local_df):
    """
    Converts all nitrogen oxide in standard unit formats, assuming that NO2 and NO are in ppb and not in µg/m³
    Air Pollutant       	     Conversion Factor	Molecular Weight
    Nitric oxide (NO)	        1 ppb = 1.23 µg/m3  	30.01 g/mol
    Nitrogen dioxide (NO2)  	1 ppb = 1.88 µg/m3	    46.01 g/mol

    """
    local_df['NO2_std'] = local_df['NO2_clean_outliers']*1.88
    local_df['NO_std'] =  local_df['NO_clean_outliers'] *1.23
    local_df['NOx_std'] =  local_df['NOx_clean_outliers']
    return local_df


def retain_as_micro(local_df):
    """
    Retains all nitrogen oxide in standard unit formats
    Air Pollutant       	     Conversion Factor	Molecular Weight
    Nitric oxide (NO)	        1 ppb = 1.23 µg/m3  	30.01 g/mol
    Nitrogen dioxide (NO2)  	1 ppb = 1.88 µg/m3	    46.01 g/mol

    """
    local_df['NO2_std'] = local_df['NO2_clean_outliers']
    local_df['NO_std'] =  local_df['NO_clean_outliers']
    local_df['NOx_std'] =  local_df['NOx_clean_outliers']
    return local_df

def unit_class(x):
    """
    assign key as blue, red, violet or yellow to each row of data
    blue:  As per CPCB norms

    red 	    ppb	    ppb	    ppb
    blue	    µg m-3	µg m-3	ppb
    violet	    µg m-3	ppb	    µg m-3
    otherwise   (retained without any changes)

    """
    if (x > 1.2):return 'blue'
    elif (x >0.9):return 'red'
    elif (x >0.5):return 'violet'
    else:return 'yellow'

def convert_cluster_wise(local_df):
    """
    assign values as per key as blue, red, violet or yellow to each row of data

    """
    local_df['NO_std'] = local_df['NO_clean']
    local_df['NO2_std'] = local_df['NO2_clean']
    local_df['NOx_std'] = local_df['NOx_clean']

    local_df.loc[local_df['score'] == 'red', 'NO_std'] = local_df['NO_clean']*1.23
    local_df.loc[local_df['score'] == 'red', 'NO2_std'] = local_df['NO2_clean']*1.88
    local_df.loc[local_df['score'] == 'red', 'NOx_std'] = local_df['NO2_clean'] + local_df['NO_clean']

    local_df.loc[local_df['score'] == 'violet', 'NO_std'] = local_df['NO_clean']*1.23
    local_df.loc[local_df['score'] == 'violet', 'NO2_std'] = local_df['NO2_clean']
    local_df.loc[local_df['score'] == 'violet', 'NOx_std'] = (local_df['NO2_clean']/1.88) + (local_df['NO_clean'])


    local_df.loc[local_df['score'] == 'blue', 'NO_std'] = local_df['NO_clean']
    local_df.loc[local_df['score'] == 'blue', 'NO2_std'] = local_df['NO2_clean']
    local_df.loc[local_df['score'] == 'blue', 'NOx_std'] = (local_df['NOx_clean'])

    return local_df


def outlier_treatment(datacolumn):
    #  sorted(datacolumn)
    """
    Provides IQR range to remove the outliers closer to the minimum value of the dataset
    """
    Q1,Q3 = np.nanpercentile(datacolumn , [25,75])
    IQR = Q3 - Q1
    lower_range = Q1 - (1.5 * IQR)
    upper_range = Q3 + (1.5 * IQR)
    return lower_range,upper_range


def find_local_outliers(local_df, col):
    """
    Finds outlier by running a 3 hour window (3*4 15 mins data)
    Median Absolute Deviation (MAD) = (value - rolling window median)

    t = |(value - rolling window median) / MAD|

    t > 3.5 --> removed as outliers

    """
    unchanged = local_df.copy(deep = True)
    local_df[col + '_clean_outliers'] = local_df[col+'_clean']
    local_df[col+'_int'] = interpolate_gaps(local_df[col].to_numpy(), limit= 2)
    local_df["med"] = local_df.groupby("StationId")[col+'_int'].rolling(window = 4*3, min_periods = 1).median().values
    local_df["med_2"] = (local_df[col+'_int'] - local_df["med"]).abs()
    local_df["mad"] = local_df.groupby("StationId")["med_2"].rolling(window = 4*3, min_periods = 1).median().values
    local_df["t"] = ((local_df[col]-local_df["med"]) / local_df["mad"]).abs()
    local_df[col+'_clean_outliers'].mask(local_df['t'] > 3.5, np.nan, inplace=True)
    local_df[col + '_clean_outliers'].mask(local_df[col] < outlier_treatment(local_df[col])[0], np.nan, inplace=True)

    for k, v in local_df.groupby((local_df[col].shift() != local_df[col]).cumsum()):
        if (len(v[col ]) >= 4) == True:
            v[col + '_clean_outliers'] = np.nan
    unchanged[col + '_clean_outliers']= local_df[col + '_clean_outliers']
    return unchanged

def find_repeats(local_df, col):
    """
    Finds repeats by running a 24 hour window (24*4 15 mins data)
    Co-efficient of Variance = Standard deviation / Mean

    t > 0.1 --> removed as repeats
    """
    unchanged = local_df.copy(deep = True)
    local_df[col+'clean'] = local_df[col]
    try:
        local_df[col+'_int'] = interpolate_gaps(local_df[col].to_numpy(), limit= 2)
    except:
        local_df[col+'_int'] = local_df[col]
        pass
    local_df[col+'_int'] = local_df[col+'_int'] +1
    local_df["med"] = local_df.groupby("StationId")[col+'_int'].rolling(window = 4*24*2, min_periods = 1).mean().values
    local_df["std"] = local_df.groupby("StationId")[col+'_int'].rolling(window = 4*24*2, min_periods = 1).std().values
    local_df["t"] = (local_df["std"]/local_df['med'])
    local_df[col+'clean'].mask(local_df['t'] < 0.1, np.nan, inplace=True)
    unchanged[col+'_clean'] = local_df[col+'clean']
#     print(local_df)
    return unchanged

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


def find_abs_rep(local_df, col, filename):

    """
    Finds absolute repeats by running a 1 hour window (1*4 15 mins data) by grouping 4 continuous constant records

    """
    unchanged = local_df.copy(deep = True)

    ar1 = interpolate_gaps(local_df[col].to_numpy(), limit=2)
    local_df[col + '_ab_rep'] = ar1
    values_repeats = []
    count_repeats = []
    starttime = []
    endtime = []
    for k, v in local_df.groupby((local_df[col + '_ab_rep'].shift() != local_df[col + '_ab_rep']).cumsum()):
        if (len(v[col + '_ab_rep']) >= 4) == True:
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
         'station_name': filename
        })
#     import pdb; pdb.set_trace()
    with open('HTMLS/' + str(filename) + ".html", 'a') as f:
        f.write(temp.sort_values(by=['count_repeats'], ascending = False)[:5].to_html())
#     temp.to_csv('absolute_repeats.csv', mode='a', index=False, header=False)
    unchanged[col + '_ab_rep'] = local_df[col + '_ab_rep']
    return unchanged



def group_plot(only_plots, local_df, col, label,station_name,filename, st_no):
#     print("group_plot")

    df_temp = find_repeats(local_df, col)
    df_temp = find_abs_rep(df_temp, col, filename)
    df = find_local_outliers(df_temp, col)



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

    figures_to_html_app([fig], filename+'.html')

    true_df = local_df.copy(deep=True)
    true_df[col+'_clean'] = df_temp[col+'_clean']
    true_df[col+'_clean_outliers'] =df[col+'_clean_outliers']
    """
    Plots the diurnal curve before and after cleaning

    """
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

    write_html_fig(fig, filename)


    return true_df


def correct_unit_inconsistency(df):
    "Converts the unit if found inconsistent with CPCB Unit reporting paramater"
    local_df = df.copy(deep =True)
    df['dates']=pd.to_datetime(df['dates'], format="%Y-%m-%d %H:%M")
    df['NOx'] =  pd.to_numeric(df.NOx, errors='coerce')
    df['NO_clean'] =  pd.to_numeric(df.NO_clean_outliers, errors='coerce')
    df['NO2_clean'] =  pd.to_numeric(df.NO2_clean_outliers, errors='coerce')
    df['NOx_clean'] =  pd.to_numeric(df.NOx_clean_outliers, errors='coerce')
    df = df[df['NO_clean'].notna()]
    df = df[df['NO2_clean'].notna()]
    df = df[df['NOx_clean'].notna()]

    X = df['NOx_clean']
    X2 = df['NOx_clean']*1/1.88
    Y1 = df["NO2_clean"] + df["NO_clean"]
    Y2 = (df["NO2_clean"]*1/1.88) + (df["NO_clean"]*1/1.23)
    Y3 =(df["NO2_clean"]*1/1.88) + (df["NO_clean"])


    local_df['ratio'] = (local_df['NO'] + local_df['NO2'])/df['NOx']
    local_df['score'] = local_df['ratio'].apply(unit_class)

    df['ratio'] = (df['NO'] + df['NO2'])/df['NOx']
    df['score'] = df['ratio'].apply(unit_class)

    fig, ax = plt.subplots()

    TEMP = local_df[local_df['score'] != 'yellow']

    ax.scatter(TEMP['NOx'], (TEMP["NO2"])*(1/1.88) + (TEMP["NO"])*(1/1.23), c = TEMP['score'].to_list())
    ax.set_title("Before unit conversion")
    ax.set_xlabel("NO" + '$_{X}$'+ '[ppb]')
    ax.set_ylabel("NO" + '$_{2}$'+ '+ NO [ppb]')
    line = mlines.Line2D([0, 1], [0, 1], color='red')
    ax.add_line(line)
    transform = ax.transAxes
    line.set_transform(transform)

    # Combine all the operations and display

    plt.show(block=False)

    options = ['C1', 'C2', 'M', '0']

    user_input = ''

    input_message = "Pick an option, pick M for mixed:\n"

    for index, item in enumerate(options):
        input_message += f'{index+1}) {item}\n'

    input_message += 'Your choice: '
    user_input = input(input_message)
    print('You picked: ' + user_input)
    if (user_input == 'C1'):
        local_df = convert_to_micro(local_df)

    elif(user_input == 'C2'):
        local_df = retain_as_micro(local_df)

    elif(user_input == 'M'):
        local_df = convert_cluster_wise(local_df)
        TEMP = local_df[local_df['score'] != 'yellow']
        TEMP.groupby(['score']).count().plot(kind='pie', y='NOx_std', colors = ['blue', 'red', 'yellow', 'violet'],
                                                 labels = ['case 2', 'case 1', 'No data', 'case 3'])


    fig, ax = plt.subplots()

    ax.scatter(TEMP['NOx_std'], (TEMP["NO2_std"])*(1/1.88) + (TEMP["NO_std"])*(1/1.23), c = TEMP['score'].to_list())
    line = mlines.Line2D([0, 1], [0, 1], color='red')
    ax.add_line(line)
    transform = ax.transAxes
    line.set_transform(transform)
    ax.set_title("After unit conversion")
    ax.set_xlabel("NO" + '$_{X}$'+ ' [ppb]')
    ax.set_ylabel("NO" + '$_{2}$'+ '+ NO [ppb]')

    plt.show()



    return local_df
