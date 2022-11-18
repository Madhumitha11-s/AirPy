import pandas as pd
import numpy as np

def get_range_for_each_window(df, col, cutoff):

    window_size = cutoff
    ran1 = []
    seq = df[col].to_numpy()
    for i in range(len(seq) - window_size + 1):
        arr = (seq[i: i + window_size]) #getting 24 hour window
        if np.isnan(arr).all() == True:
            ran1.append(np.nan)

        else:
#             arr = interpolate_gaps(arr, limit=2)
            ran1.append(rolling_range(arr))

    ran2 = []
    seq = df[col].to_numpy()
    seqr = seq[::-1]
    for i in range(len(seqr) - window_size + 1):
        arr = (seqr[i: i + window_size]) #getting 24 hour window
        if np.isnan(arr).all() == True:
            ran2.append(np.nan)

        else:
            arr = interpolate_gaps(arr, limit=2)
            ran2.append(rolling_range(arr))

    last_part = len(seq) - len(ran1) # take these many entries from reversed data and reverse it to append in main data
    ran2 = ran2[0: last_part][::-1] #reveresed the last parts
    ran1 = ran1 + (ran2)

    return ran1

def rolling_range(arr):
    """
    Here arr is the 24 hour window running values

    """

    return (np.nanmax(arr) - np.nanmin(arr))

def rolling_window(df, col, t, cutoff):

    window_size = cutoff
    seq = df[col].to_numpy()
    outlier = 0
    ran = []



    if (len(seq) < 4*24) == True:
        window_size = len(seq) - 1

    for i in range(len(seq) - window_size + 1):
        arr = (seq[i: i + window_size]) #getting 24 hour window
        arr = interpolate_gaps(arr, limit=2)
        ran.append(rolling_range(arr))


    for i in range(len(seq) - window_size + 1):
        arr = (seq[i: i + window_size]) #getting 24 hour window
        out = outlier_mad(arr) #call the mad method for that particular 24 hour window
        (seq[i: i + window_size]) = out[0] #store the cleaned data in seq
        outlier = outlier + out[1] #store the outlier total
    print("There is/ are ", outlier, "in ", str(col), " in total upon 24 hour window")
    print("There is/ are ", outlier_mad(seq)[1], "in ", str(col), " in when considered in total")

    return

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

def get_clean_by_range(local_df, col,col_name,station_name, t, cutoff):


    local_df[col + '_range'] = get_range_for_each_window(local_df, col, cutoff)

    local_df[col + '_label']= np.where(local_df[col + '_range']<= t, 0, np.nan )


    local_df[col + '_clean'] = local_df[col]
    for k, v in local_df.groupby((local_df[col + '_range'].shift() != local_df[col + '_range']).cumsum()):
        if (len(v) >= cutoff) == True:
            local_df['hint'] = local_df.dates.between((v['dates'].iloc[0]), (v['dates'].iloc[-1]))
            local_df[col +'_clean'] = np.where(local_df['hint'] == True, np.nan,local_df[col + '_clean'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col],opacity=0.5,marker=dict(color = 'red', size = 3.5),
                        mode='markers', name='actual'))

    fig.add_trace(go.Scatter(x=local_df['dates'], y=local_df[col + '_clean'],opacity=0.5,marker=dict(color = 'blue', size = 3.5),
                        mode='markers', name='clean'))
    fig.update_layout(legend= {'itemsizing': 'constant'}, template = "simple_white")
    fig.update_layout(xaxis_title="Date", yaxis_title= str(col_name) + " concentration in µg/m³")
    fig.update_layout(legend=dict(yanchor="top",xanchor="left"))
    figures_to_html_app([fig], station_name+ '.html')

    return
