import pandas as pd
import numpy as np
def get_threshold_so2(df):
    local_df = df.copy(deep = True)

    df_new = df[['SO2', 'dates']].copy()

    c = 0
    s_date = []
    e_date = []
    thre = []
    rang = len(df_new) / (24*4 + 24*4 + 24*4)
    for i in range(int(rang - 1)):
        try:
            temp = df_new[c: c +i+24*4*3]
            cosn = temp['SO2'].std()/temp['SO2'].mean()
            e_date.append(df_new['dates'][c +i+24*4*3])
            thre.append(cosn)
            s_date.append(df_new['dates'][c])
            import pdb; pdb.set_trace()


            c = c +i+24*4*3
        except:
            pass
    so2_thr = pd.DataFrame({'thre': thre,'s_date': s_date,'e_date': e_date})


    so2_thr = so2_thr[(so2_thr['thre'] <= 0.1)].reset_index()
    del so2_thr['index']
    col = 'SO2'
    import pdb; pdb.set_trace()


    df[col+'_cleaned'] = df[col]
    for i in range(len(so2_thr)):
        df[col+'_cleaned'] = np.where((df['dates'] >= so2_thr['s_date'][i]) &(df['dates'] < so2_thr['e_date'][i]) , np.nan, df[col+'_cleaned'])

    local_df[col+'_cleaned_3days'] = df[col+'_cleaned']

    return local_df
