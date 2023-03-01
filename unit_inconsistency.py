import pandas as pd
import numpy as np
import plotly.graph_objs as go
from html_utils import *
from plot_diurnal import *
import csv
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


"""
Returns a unique LABEL for each color

"""
def color_to_case(argument):
    
    """
    function return the actual unit of each row based on keys assigned
    
    Parameter
    ---------
    argument: string
        annual 15 mins pollutant data 
        
        
    return
    ------
    switcher: gets corresponding keys for the given string argument
      
    """

    switcher = {"red": "Case 1 (NO: ppb; NO2: ppb; NOx: ppb)",
                "blue": "Case 2 (CPCB Standards: NO: µg m-3; NO2: µg m-3; NOx: ppb)",
                "green": "Case 3 (NO:µg m-3; NO2: ppb; NOx: µg m-3)",
                "violet": "Case 4 (NO:µg m-3; NO2: ppb; NOx: µg m-3)"}
    return switcher.get(argument, "nothing")


def convert_to_micro(local_df):
    
    """
    function converts NO, NO2 in ppb to µg/m3
    
    Parameter
    ---------
    local_df: pandas column
        annual 15 mins pollutant data 
        
        
    return
    ------
    local_df: pandas column
        input local_df adjusted with conversion factors 
    
    Converts all nitrogen oxide in standard unit formats, assuming that NO2 and NO are in ppb and not in µg/m³
    +----------------------+----------------------+----------------------+
    |     Air Pollutant    |   Conversion Factor  |         Weight       |
    +----------------------+----------------------+----------------------+
    |  Nitric oxide (NO)   | 1 ppb = 1.23 µg/m3   |      30.01 g/mol     |
    |Nitrogen dioxide (NO2)| 1 ppb = 1.88 µg/m3   |      46.01 g/mol     |
    +----------------------+----------------------+----------------------+

    
    Reference
    ---------
    .. [1] Heinecke, R. (2022, August 3). Air pollution – How to convert between mg/m3, µg/m3 and ppm, ppb. 
    Breeze Technologies. https://www.breeze-technologies.de/blog/air-pollution-how-to-convert-between-mgm3-%C2%B5gm3-ppm-ppb/
    
    """

    local_df['NO2_CPCB'] = local_df['NO2_outliers']*1.88
    local_df['NO_CPCB'] =  local_df['NO_outliers'] *1.23
    local_df['NOx_CPCB'] =  local_df['NOx_outliers']
    return local_df


def retain_as_micro(local_df):
    """
    Retains all nitrogen oxide in standard unit formats
        
    Parameter
    ---------
    local_df: pandas column
        annual 15 mins pollutant data 
        
        
    return
    ------
    local_df: pandas column
        input local_df adjusted with conversion factors 
    
    Converts all nitrogen oxide in standard unit formats, assuming that NO2 and NO are in ppb and not in µg/m³
    +----------------------+----------------------+----------------------+
    |     Air Pollutant    |   Conversion Factor  |         Weight       |
    +----------------------+----------------------+----------------------+
    |  Nitric oxide (NO)   | 1 ppb = 1.23 µg/m3   |      30.01 g/mol     |
    |Nitrogen dioxide (NO2)| 1 ppb = 1.88 µg/m3   |      46.01 g/mol     |
    +----------------------+----------------------+----------------------+

    
    Reference
    ---------
    .. [1] Heinecke, R. (2022, August 3). Air pollution – How to convert between mg/m3, µg/m3 and ppm, ppb. 
    Breeze Technologies. https://www.breeze-technologies.de/blog/air-pollution-how-to-convert-between-mgm3-%C2%B5gm3-ppm-ppb/
    
    """

    local_df['NO2_CPCB'] = local_df['NO2_outliers']
    local_df['NO_CPCB'] =  local_df['NO_outliers']
    local_df['NOx_CPCB'] =  local_df['NOx_outliers']
    return local_df


def unit_class(x):
    
        
    """
    function to identify the reported unit of each row of data 
    
    Parameter
    ---------
    x: list
        ratio of NO + NO2 to NOx  
        
        
    return
    ------
    keys: strings
        different colors for different unit combinations
    
    Converts all nitrogen oxide in standard unit formats, assuming that NO2 and NO are in ppb and not in µg/m³

    +---------+--------+-------+-------+   
    |         |   NO   |  NO2  |  NOx  |
    +---------+--------+-------+-------+
    |   red   |  ppb   |  ppb  |  ppb  |
    |   blue  | µg m-3 | µg m-3|  ppb  |
    |  violet | µg m-3 |  ppb  |µg m-3 |
    |  green  |  both  |µg m-3 |  both |
    +---------+--------+-------+-------+   
    | otherwise                        |
    | (retained without any changes)   |
    +---------+--------+-------+-------+    
    
    
    Reference
    ---------
    .. [1] Heinecke, R. (2022, August 3). Air pollution – How to convert between mg/m3, µg/m3 and ppm, ppb. 
    Breeze Technologies. https://www.breeze-technologies.de/blog/air-pollution-how-to-convert-between-mgm3-%C2%B5gm3-ppm-ppb/
    

    """
    if (x > 1.85):return 'green'
    elif (x > 1.25):return 'blue'
    elif (x >0.8):return 'red'
    elif (x >0.5):return 'violet'
    elif (x == np.nan):return 'yellow'
    else:return 'yellow'
    
    
def clean_dataset(df):
    """
    functions cleans the dataset for invalid entries

    code credits: Boern, Technical Data Specialist at MunichRe
    sklearn error ValueError: Input contains NaN, infinity or a value too large for dtype('float64’). (n.d.). 
    Stack Overflow. https://stackoverflow.com/questions/31323499/sklearn-error-valueerror-input-contains-nan-
    infinity-or-a-value-too-large-for

    returns the dataframe as float

    """

    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    return df[indices_to_keep].astype(np.float64)   

def convert_cluster_wise(local_df):
    """
    Adjusts the values as per cases (blue, red, violet or yellow) when user specifies "M" as cluster condition
    
    Parameter
    ---------
    local_df: pandas column
        annual 15 mins pollutant data 
        
        
    return
    ------
    local_df: pandas column
        input local_df adjusted with conversion factors 

    
    Following are the cases 

    +---------+--------+-------+-------+   
    |         |   NO   |  NO2  |  NOx  |
    +---------+--------+-------+-------+
    |   red   |  ppb   |  ppb  |  ppb  |
    |   blue  | µg m-3 | µg m-3|  ppb  |
    |  violet | µg m-3 |  ppb  |µg m-3 |
    |  green  |  both  |µg m-3 |  both |
    +---------+--------+-------+-------+   
    | otherwise (yellow)               |
    | (retained without any changes)   |
    +---------+--------+-------+-------+    
    
    Records assigned with class as green could be of two types wherein, NO and NOx are in incorrect units or either one of them are in incorrect units. Finally, appropriate units combination whoes mean square error is the least are assigned.
        
    Reference
    ---------
    .. [1] Heinecke, R. (2022, August 3). Air pollution – How to convert between mg/m3, µg/m3 and ppm, ppb. 
    Breeze Technologies. https://www.breeze-technologies.de/blog/air-pollution-how-to-convert-between-mgm3-%C2%B5gm3-ppm-ppb/
    

                

    """
    
    #copy the raw data 
    local_df['NO_CPCB'] = local_df['NO_consecutives']
    local_df['NO2_CPCB'] = local_df['NO2_consecutives']
    local_df['NOx_CPCB'] = local_df['NOx_consecutives']

    #adjust the data based on categories
    local_df.loc[local_df['score'] == 'red', 'NO_CPCB'] = local_df['NO_outliers']*1.23
    local_df.loc[local_df['score'] == 'red', 'NO2_CPCB'] = local_df['NO2_outliers']*1.88
    local_df.loc[local_df['score'] == 'red', 'NOx_CPCB'] = local_df['NO2_outliers'] + local_df['NO_outliers']

    local_df.loc[local_df['score'] == 'violet', 'NO_CPCB'] = local_df['NO_outliers']*1.23
    local_df.loc[local_df['score'] == 'violet', 'NO2_CPCB'] = local_df['NO2_outliers']
    local_df.loc[local_df['score'] == 'violet', 'NOx_CPCB'] = (local_df['NO2_outliers']/1.88) + (local_df['NO_outliers'])

    
    #adjust the data classified as green 
    TEMP = local_df[local_df['score'] == 'green']
    if len(TEMP) > 20:
        
        
        TEMP = clean_dataset(TEMP[['NO', 'NO2', 'NOx']])
        X1 = TEMP['NOx'].values.astype(np.float)
        y1 =  ((TEMP["NO2"])*(1/1.88) + (TEMP["NO"])*(1/1.23)/1.23).values.astype(np.float)

        X2 = (TEMP['NOx']*1.9125).values.astype(np.float)
        y2 =  ((TEMP["NO2"])*(1/1.88) + (TEMP["NO"])*(1/1.23)).values.astype(np.float)

        #check for mean square error to determine the good fit
        if mean_squared_error(X1, y1) < mean_squared_error(X2, y2):
            local_df.loc[local_df['score'] == 'green', 'NO_CPCB'] = local_df['NO_outliers']/1.23
            local_df.loc[local_df['score'] == 'green', 'NO2_CPCB'] = local_df['NO2_outliers']
            local_df.loc[local_df['score'] == 'green', 'NOx_CPCB'] = local_df['NOx_outliers']
        else: 
            local_df.loc[local_df['score'] == 'green', 'NO_CPCB'] = local_df['NO_outliers']
            local_df.loc[local_df['score'] == 'green', 'NO2_CPCB'] = local_df['NO2_outliers']
            local_df.loc[local_df['score'] == 'green', 'NOx_CPCB'] = local_df['NOx_outliers']*1.9125


    local_df.loc[local_df['score'] == 'blue', 'NO_CPCB'] = local_df['NO_outliers']
    local_df.loc[local_df['score'] == 'blue', 'NO2_CPCB'] = local_df['NO2_outliers']
    local_df.loc[local_df['score'] == 'blue', 'NOx_CPCB'] = (local_df['NOx_outliers'])

    return local_df


def correct_unit_inconsistency(df,filename, get_input):
    
    """
    Adjusts the values as per cases (blue, red, violet or yellow) when user specifies "M" as cluster condition 
    
    Parameter
    ---------
    local_df: pandas column
        annual 15 mins pollutant data 
        
        
    return
    ------
    local_df: pandas column
        input local_df adjusted with conversion factors 

    NO and NO2 are supposed to be reported in µg/m3 in the CCR portal. 
    However, we find instances where sites largely misreports NO and NO2 in ppb.
    Converts the unit if found inconsistent with CPCB Unit reporting paramater
    
    Interestingly, certain sites, reports the data in correct units in few months and starts to misreport in other unit combinations for other months. This makes it difficult to classify the data points, as many data reporting formats are within same dataset. 
    In our datasets, we observed four unit types while reporting the NO, NO2 and NOx data. 
    This function returns all the three parameters in ppb and CPCB standard reporting units, after identifing the actual unit.
    
    Ratio of NO + NO2 / NOx is primarily employed in identifying the reporting unit. 
    
    Following are the cases 

    +---------+--------+-------+-------+   
    |         |   NO   |  NO2  |  NOx  |
    +---------+--------+-------+-------+
    |   red   |  ppb   |  ppb  |  ppb  |
    |   blue  | µg m-3 | µg m-3|  ppb  |
    |  violet | µg m-3 |  ppb  |µg m-3 |
    |  green  |  both  |µg m-3 |  both |
    +---------+--------+-------+-------+   
    | otherwise (yellow)               |
    | (retained without any changes)   |
    +---------+--------+-------+-------+    
    
    Records assigned with class as green could be of two types wherein, NO and NOx are in incorrect units or either one of them are in incorrect units. Finally, appropriate units combination whoes mean square error is the least are assigned.
        
    Reference
    ---------
    .. [1] Heinecke, R. (2022, August 3). Air pollution – How to convert between mg/m3, µg/m3 and ppm, ppb. 
    Breeze Technologies. https://www.breeze-technologies.de/blog/air-pollution-how-to-convert-between-mgm3-%C2%B5gm3-ppm-ppb/
    

                

    """


    
    #create a deep copy of df, hence all the computation inside the df will not affect the copy local_df or vice versa
    local_df = df.copy(deep =True)
    
    #format the dates column in years-month-date hours-minutes format
    df['dates']=pd.to_datetime(df['dates'], format="%Y-%m-%d %H:%M")
    
    # invalid parsing or null entries will be set as NaN
    df['NOx'] =  pd.to_numeric(df.NOx, errors='coerce') 
    df['NO_consecutives'] =  pd.to_numeric(df.NO_outliers, errors='coerce')
    df['NO2_consecutives'] =  pd.to_numeric(df.NO2_outliers, errors='coerce')
    df['NOx_consecutives'] =  pd.to_numeric(df.NOx_outliers, errors='coerce')
    
    # remove all rows even if any one of the oxides of nitrogen data is NaN
    df = df[df['NO_consecutives'].notna()]
    df = df[df['NO2_consecutives'].notna()]
    df = df[df['NOx_consecutives'].notna()]
    
    
    # ratio is calculated by dividing the sum of reported NO and NO2 by reported NOx
    df['ratio'] = (df['NO'] + df['NO2'])/df['NOx']
    
    #based on ratio calculated, a separate category is assigned using the fuction unit class
    df['score'] = df['ratio'].apply(unit_class)
    
    #if no unit is identified for that particular row, assign a dummy category "yellow"
    df['score'] = df['score'].replace(np.nan, 'yellow')

    
    # Using NO + NO2 = NOx (ppb); assume that NO2 is incorrectly reported in ppb
    df['score'].mask((((df['NO'])/1.23 + (df['NO2']) - (df['NOx'])).abs() < 5), 'green', inplace=True)
    
    # Using NO + NO2 = NOx (ppb); assume that NO2, NO is incorrectly reported in ppb
    df['score'].mask((((df['NO']) + (df['NO2']) - (df['NOx'])).abs() < 5), 'red', inplace=True)
    
    # Using NO + NO2 = NOx (ppb); assume that all are correctly reported according to CPCB standards
    df['score'].mask((((df['NO'])/1.23 + (df['NO2'])/1.88 - (df['NOx'])).abs() < 5), 'blue', inplace=True)
    
    
    #repeat the above steps in deep copy dataframe
    local_df['ratio'] = (local_df['NO'] + local_df['NO2'])/local_df['NOx']
    local_df['score'] = local_df['ratio'].apply(unit_class)
    local_df['score'] = local_df['score'].replace(np.nan, 'yellow')
    local_df['score'].mask((((local_df['NO']) + (local_df['NO2']) - (local_df['NOx'])*1.9125).abs() < 5), 'green', inplace=True)
    local_df['score'].mask((((local_df['NO']) + (local_df['NO2']) - (local_df['NOx'])).abs() < 5), 'red', inplace=True)
    local_df['score'].mask((((local_df['NO'])/1.23 + (local_df['NO2'])/1.88 - (local_df['NOx'])).abs() < 5), 'blue', inplace=True)
   
    
    
    #Plot the NOx and sum of NO and NO2 in ppb, assuming the reported units are correct
    fig, ax = plt.subplots()
    
    #remove all rows, for which units are not identified
    TEMP = df[df['score'] != 'yellow']

    ax.scatter(TEMP['NOx'], (TEMP["NO2"])*(1/1.88) + (TEMP["NO"])*(1/1.23), c = TEMP['score'].to_list())
    ax.set_title("Before unit conversion")
    ax.set_xlabel("NO" + '$_{X}$'+ '[ppb]')
    ax.set_ylabel("NO" + '$_{2}$'+ '+ NO [ppb]')
    
    #plot a solid black 1:1 line 
    plt.plot([1, np.nanmax(TEMP['NOx'])],[1,np.nanmax(TEMP['NOx'])], c = 'black')


    #upload the figure in HTML
    write_html_fig(fig, filename)
    
    #Show the image to the user even inside the loop
    plt.show(block=False)    
    
    
    options = ['C1 (red)', 'C2 (blue)', 'M (many clusters)', '0 (None)']
    user_input = ''
    
    #allows the user to choose "M" as default and manual clustering    
    if get_input == True:
        
        print("red: Case 1 (NO: ppb; NO2: ppb; NOx: ppb) \n",
              "blue: Case 2 (CPCB Standards: NO: µg m-3; NO2: µg m-3; NOx: ppb) \n",
              "violet: Case 3 (NO:µg m-3; NO2: ppb; NOx: µg m-3 \n",
              "green: Case 4 (NO:µg m-3; NO2: µg m-3; NOx: µg m-3 \n")        

        input_message = "Pick an option, pick M for mixed:\n"

        for index, item in enumerate(options):
            input_message += f'{index+1}) {item}\n'
        input_message += 'Your choice: '
        user_input = input(input_message)
        print('You picked: ' + user_input)
    else:
        user_input = 'M'
        

        
    if (user_input == 'C1') or (user_input == 'c1'):
        local_df = convert_to_micro(local_df)
    elif(user_input == 'C2') or (user_input == 'c2'):
        local_df = retain_as_micro(local_df)
    elif(user_input == 'M') or (user_input == 'm'):
        local_df = convert_cluster_wise(local_df)
        
        #Show the different clusters identified in scatter plot and pie chart
        TEMP = local_df[local_df['score'] != 'yellow']
        color = TEMP.groupby(['score']).count().index.to_list()
        label = []
        for name in color:
            label += [color_to_case(name)]    
        TEMP.groupby(['score']).count().plot(kind='pie', y='NOx_CPCB', colors = color,
                                                 labels = label)

    #show the scatter plot post unit correction
    fig, ax = plt.subplots()
    TEMP = local_df[local_df['score'] != 'yellow']
    ax.scatter(TEMP['NOx_CPCB'], (TEMP["NO2_CPCB"])*(1/1.88) + (TEMP["NO_CPCB"])*(1/1.23), c = TEMP['score'].to_list())    
    #Plot a 1:1 line
    plt.plot([1, np.nanmax(TEMP['NOx_CPCB'])],[1,np.nanmax(TEMP['NOx_CPCB'])], c = 'black')
    ax.set_title("After unit conversion")
    ax.set_xlabel("NO" + '$_{X}$'+ ' [ppb]')
    ax.set_ylabel("NO" + '$_{2}$'+ '+ NO [ppb]')
    #upload the figure in the HTML
    write_html_fig(fig, filename)
    plt.show(block=False)
    
    #format all the data in ppb    
    local_df['NO_ppb'] = (local_df["NO_CPCB"])*(1/1.23)
    local_df['NO2_ppb'] = (local_df["NO2_CPCB"])*(1/1.88)
    local_df['NOx_ppb'] = (local_df["NOx_CPCB"])



    return local_df
