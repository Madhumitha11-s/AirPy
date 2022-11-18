import pandas as pd
import numpy as np
def rep24(local_df, col):

    df_grouped = get_group(local_df, col)
    df = pd.merge(local_df, df_grouped, how ='outer', on = 'date')
    df[col+'24hr'] = np.where(df['std_mean'] <= 0.12, np.nan, local_df[col])
    df = df[[col+'24hr', 'date', 'std_mean']].copy()

    return df


def get_group(df, col):

    #https://stackoverflow.com/questions/53179216/pandas-group-by-and-sum-every-n-rows
#         df[col] = np.where(df[col] <= 2,  local_df[col] + 5 , local_df[col])


    df_grouped = (df[[col]].groupby(df['dates'].dt.date).agg(['mean', 'std', 'count', 'min', 'max']))
    df_grouped = df_grouped.droplevel(axis=1, level=0).reset_index()
    # Calculate a confidence interval as well.
    df_grouped['ci'] = 1.96 * df_grouped['std'] / np.sqrt(df_grouped['count'])
    df_grouped['ci_lower'] = df_grouped['mean'] - df_grouped['ci']
    df_grouped['ci_upper'] = df_grouped['mean'] + df_grouped['ci']
    df_grouped['range'] = df_grouped['max'] + df_grouped['min']
    df_grouped['std_mean'] = df_grouped['std'] / df_grouped['mean']
    df_grouped['date'] = df_grouped['dates']
    df_grouped = df_grouped[['std_mean', 'date']].copy()
    return df_grouped
