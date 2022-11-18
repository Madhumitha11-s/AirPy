df_2 = local_df.copy(deep=True)
col = 'PM25'


window_size = 1*4*24
seq = df_2[col].to_numpy()
ratio = []
# seq = np.concatenate((np.asarray([[np.nan]*48]), seq), axis=None)


for i in range(len(seq) - window_size + 1):
    arr = (seq[i: i + window_size]) #getting 24 hour window
#     print(seq[i], seq[i + window_size])
    t = np.nanstd(arr)/ np.nanmedian(arr)
    ratio.extend([t])

ratio = np.concatenate((np.asarray([[np.nan]*48]), ratio), axis=None)
len_x = len(df_2) - len(ratio)
ratio = np.concatenate(  ( ratio, np.asarray([[np.nan]*len_x]) )  , axis=None)

df = pd.DataFrame()
df[col] = df_2[col]

df['dates'] = df_2['dates']
df["ratio"] = ratio
df[col + '_clean']= np.where(df['ratio'] <= 0.1, np.nan, df_2[col])

fig = go.Figure()

df[col + '_label_binary']= np.where(df['ratio'] <= 0.1, 0, 1)

df[col + '3hour_res'] = df_2[col]

df[col + '_label'] = np.random.randint(10,100, size=len(df))
df[col + '_label']= np.where(df['ratio'] <= 0.1, 0, df[col + '_label'])
for k, v in df.groupby((df[col + '_label'].shift() != df[col + '_label']).cumsum()):
    if (len(v[col + '_label']) >= 12) == True:
        df['hint'] = df.dates.between((v['dates'].iloc[0]), (v['dates'].iloc[-1]))
        df[col+ '3hour_res'] = np.where(df['hint'] == True, np.nan, df[col+ '3hour_res'])




fig = go.Figure()

fig.add_trace(go.Scatter(x=df['dates'], y=  df[col + '_label_binary'],mode='lines', name='label'))
fig.add_trace(go.Scatter(x=df['dates'], y=df[col],mode='markers', name='actual',marker=dict( size = 1)))
fig.add_trace(go.Scatter(x=df['dates'], y=df[col+'_clean'], mode='markers', name='running_algo_with_ratio',marker=dict( size = 1)))
figures_to_html_app([fig], 'temp'+ '.html')
# fig.add_trace(go.Scatter(x=df['dates'], y=df[col+'3hour_res'], mode='lines', name='running_algo_with_ratio + 3hr restriction'))
