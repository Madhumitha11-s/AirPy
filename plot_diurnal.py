'''
Get grouped returns the column with confidence interval with lower and upper bounds


'''

import pandas as pd
import numpy as np
"""
Plots diurnal curve for pollutant
Upper and lower boundaries denotes confidence interval (95%)
"""
def get_grouped(df, col):
    df_grouped = (df[[col]].groupby(df['dates'].dt.hour).agg(['mean', 'std', 'count']))
    df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
    # Calculate a confidence interval as well.
    df_grouped['ci'] = 1.96 * df_grouped['std'] / np.sqrt(df_grouped['count'])
    df_grouped['ci_lower'] = df_grouped['mean'] - df_grouped['ci']
    df_grouped['ci_upper'] = df_grouped['mean'] + df_grouped['ci']

    return df_grouped

def plot_diurnal(df_grouped, color, pollutant, ax):
    x = df_grouped['dates']
    # fig, ax = plt.subplots()
    ax.plot(x, df_grouped['mean'],color = str(color), label = pollutant)
    ax.fill_between(x, df_grouped['ci_lower'], df_grouped['ci_upper'], color = str(color), alpha=.15)
    ax.legend(loc='upper right')
    ax.set_ylim(ymin=0)
    return ax

def get_diurnal(df, pollutant, color, title, ax):
    df_grouped_NO = get_grouped(df, pollutant)
    plot_diurnal(df_grouped_NO, color, pollutant, ax)
    return
