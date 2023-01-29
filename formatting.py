import pandas as pd
import numpy as np
import pandas as pd

def get_formatted_df(path):
    try:
        station_name = path.split("\\")[-1].split("_")[0].replace(".csv", "")
    except:
        station_name = path.split("\\")[-1].replace(".csv", "")
        pass
    try:
        df = pd.read_csv(path)
        try:
            station_name = path.split("\\")[-1].split("_")[0].replace(".csv", "")
        except:
            station_name = path.split("\\")[-1].replace(".csv", "")
            pass

    except:
        try:
            df = pd.read_excel(path)
            df, from_date, to_date, station_name = get_multiple_df_linerized(df)
        except:
            print("provide data in specified formats")
            pass
    df = read_df(df)
    df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
    return df, station_name



def read_df(df):
    if 'dates' in df.columns:
        try:
            df['dates']=pd.to_datetime(df['dates'], format="%Y-%m-%d %H:%M")
        except:
            df['dates']=pd.to_datetime(df['dates'], format="%d-%m-%Y %H:%M")
            pass
    elif 'date' in df.columns:
        try:
            df['date']=pd.to_datetime(df['date'], format="%Y-%m-%d %H:%M")
        except:
            df['date']=pd.to_datetime(df['date'], format="%d-%m-%Y %H:%M")
            pass
    else:
        try:
            df['dates']=pd.to_datetime(df['From Date'], format="%Y-%m-%d %H:%M")
        except:
            try:
                df['dates']=pd.to_datetime(df['From Date'], format="%d-%m-%Y %H:%M")
            except:
                "date formats not matching"
                pass
            pass
    try:
        df['PM10'] =  pd.to_numeric(df.PM10, errors='coerce')
    except:
        print("NO PM10 data")
        df['PM10'] = np.nan
        pass
    try:
        df['NO'] =  pd.to_numeric(df.NO, errors='coerce')
    except:
        print("No NO data")
        df['NO'] = np.nan
        pass
    try:
        df['NO2'] =  pd.to_numeric(df.NO2, errors='coerce')
    except:
        print("No NO2 data")
        df['NO2'] = np.nan
        pass
    try:
        df['NOx'] =  pd.to_numeric(df.NOx, errors='coerce')
    except:
        print("NO NOx data")
        df['NOx'] = np.nan
        pass
    try:
        df['Ozone'] =  pd.to_numeric(df.Ozone, errors='coerce')
    except:
        print("NO Ozone data")
        df['Ozone'] = np.nan
        pass
    try:
        df['PM25'] =  pd.to_numeric(df.name, errors='coerce')
    except:
        try:
            df.rename(columns = {'PM2.5':'PM25'}, inplace = True)
            df['PM25'] =  pd.to_numeric(df.PM25, errors='coerce')
        except:
            df['PM25'] = np.nan
            print("NO PM data")
            pass
    return df





def get_multiple_df_linerized(df1):

    "Used to format the direct CPCB output"
    
    from_year = df1['Unnamed: 1'][8][6:10]
    to_year = df1['Unnamed: 1'][9][6:10]
    station_name = df1['CENTRAL POLLUTION CONTROL BOARD'][11]
    lst = df1.index[df1['CENTRAL POLLUTION CONTROL BOARD'] == "From Date"].tolist()
    count = 1
    for i in range(len(lst)):
        if (i+1 == len(lst)):
            df_temp = df1[lst[i]:].reset_index(drop=True)
        else:
            df_temp = df1[lst[i]:lst[i+1]-1].reset_index(drop=True)
        df_temp = df_temp.rename(columns=df_temp.iloc[0]).drop(df_temp.index[0])
        df_temp = df_temp.loc[:, df_temp.columns.notna()]
        if count != 1:
            del df_temp['From Date'],  df_temp['To Date']
            df_concat = pd.concat([df_concat, df_temp], axis=1)
        else:
            df_concat = df_temp
        count = count + 1
    df_concat = df_concat.rename(columns = {'PM2.5':'PM_25', 'From Date':'dates'})
    del df_concat['To Date']
    df_concat = df_concat[:len(df1[lst[0]:df1.index[df1['CENTRAL POLLUTION CONTROL BOARD'] == "Prescribed Standards"].tolist()[1]-1].reset_index(drop=True))-1]
    return df_concat, from_year, to_year,station_name
