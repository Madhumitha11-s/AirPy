from pathlib import Path
import pandas as pd
import csv
import pandas as pd
import os
from data_cleaning import *
from sub_super_script import *
from html_utils import *
from formatting import *
from init_html import *
from plot_diurnal import *
from unit_inconsistency import *
from numbers_to_strings import *
import warnings
warnings.filterwarnings("ignore")

from termcolor import *
from main import  clean_dataset
def clean_dataset(year, main_directory, mixed_unit_identification):
    
    #creating a new directory called HTMLS, After_cleaning, before_cleaning
    Path(main_directory + "\HTMLS").mkdir(parents=True, exist_ok=True)
    Path(main_directory + "\After_Cleaning").mkdir(parents=True, exist_ok=True)
    Path(main_directory + "\Before_Cleaning").mkdir(parents=True, exist_ok=True)
    directory = main_directory + "\Before_Cleaning"
    
    
    for filename in os.listdir(directory):
        path = os.path.join(directory, filename) 
        true_df, station_name, city, state = get_formatted_df(path)
        year = 2020
        true_df = true_df[true_df['dates'].dt.year == year]
        true_df = true_df.loc[~true_df.index.duplicated(keep='first')]

        df = true_df.copy(deep=True)

        filename=station_name+"_"+str(year) 
        start_html(filename)


        st_no = numbers_to_strings(station_name)
        print(colored("===========================================================================================", 'magenta', attrs=['bold']))
        print(colored(station_name,  'magenta', attrs=['bold']))
        print(colored("===========================================================================================", 'magenta', attrs=['bold']))





        only_plots = true_df.copy(deep=True)
        local_df = true_df.copy(deep=True)

        local_df['date'] =  pd.to_datetime(local_df['dates']).dt.date
        local_df = local_df.sort_values(by=['dates'])
        local_df = local_df[local_df['date'].notna()]
        local_df['StationId'] = station_name
        local_df['city'] = city
        local_df['state'] = state
        lst = ['PM25', 'PM10', 'NOx', 'NO2', 'NO', 'Ozone' ]
    #     lst = ['NOx', 'NO2', 'NO' ]
        for name in lst:
            if len(df[name].value_counts()) == 0:
                print("No available ", name, " data")
                continue
            else:

                try:

                    local_df = group_plot(only_plots, local_df, name, name,station_name,filename, st_no)                 
                    local_df[name + '_hourly'] = local_df.groupby("StationId")[name].rolling(window = 4*1, min_periods = 1).mean().values
                    local_df[name + '_clean'] = local_df[name + '_outliers']
                    local_df[name + '_clean'].mask(local_df[name+ '_hourly'] < 0, np.nan, inplace=True)

                    del local_df[name + '_hourly']

                    print("successfully cleaned ", name, " ", station_name)

                except:

                    print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))
                    print(colored('error in ' + name + " " + station_name,  'red', attrs=['bold']))
                    print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))
                    pass
        try:
            local_df = correct_unit_inconsistency(local_df,filename, mixed_unit_identification)
            del local_df['score']
            for name in lst:
                del  local_df[name + '_outliers'], local_df[name + '_consecutives'], local_df[name + 'consecutives'],local_df[name + '_int']
        except:
            import pdb; pdb.set_trace()
            print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))
            print(colored('error in unit identification for' + name + " " + station_name,  'red', attrs=['bold']))
            print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))

            
        try:
            
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_outliers')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_consecutives')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_int')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='consecutives')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='_outliers')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='med')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='std')))]
            local_df = local_df[local_df.columns.drop(list(local_df.filter(regex='t')))]


        except:

            print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))
            print(colored('Unable to delete unnecessary data' + " " + station_name,  'red', attrs=['bold']))
            print(colored("----------------------------------------------------------------------------------------", 'red', attrs=['bold']))

            
            pass
        
        local_df.to_csv(str("After_Cleaning\\") + str(station_name) +'_'+ str(year)+ ".csv")

        print(colored("----------------------------------------------------------------------------------------", 'green', attrs=['bold']))
        print(colored('saved successfully for'  + station_name,  'green', attrs=['bold']))
        print(colored("----------------------------------------------------------------------------------------", 'green', attrs=['bold']))
        


        
        

