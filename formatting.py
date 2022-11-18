import pandas as pd
import numpy as np
import pandas as pd

def get_formatted_df(path):
    year = (path.split('_')[3]).split('.')[0]
    station_name = (path.split('\\')[4]).split('_')[0]
    df = pd.read_csv(path)
    df['dates']=pd.to_datetime(df['From Date'], format="%d-%m-%Y %H:%M")
    if 'PM2.5' in df.columns:
        df.rename(columns = {'PM2.5':'PM25'}, inplace = True)
    else:
        print("")

    del df['From Date']
    del df['To Date']

    df['SO2'] =  pd.to_numeric(df.SO2, errors='coerce')
    df['NOx'] =  pd.to_numeric(df.NOx, errors='coerce')
    df['Ozone'] =  pd.to_numeric(df.Ozone, errors='coerce')
    df['NO2'] =  pd.to_numeric(df.NO2, errors='coerce')

    df['PM10'] =  pd.to_numeric(df.PM10, errors='coerce')
    df['PM25'] =  pd.to_numeric(df.PM25, errors='coerce')
    df['NO'] =  pd.to_numeric(df.NO, errors='coerce')


    return df, station_name, year
