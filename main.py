import pandas as pd
from group_functions import *
from sub_super_script import *
from html_utils import *
from std_mean_ratio_method import *
from range_method import *
from formatting import *
from init_html import *
warnings.filterwarnings("ignore")

directory = r'E:\MTech_Project\CPCB_Datavalidation\df_csv'

# iterate over files in
# that directory
for filename in os.listdir(directory):
    path = os.path.join(directory, filename)

    # path =r"E:\MTech_Project\CPCB_Datavalidation\Data\Bandra, Mumbai - MPCB_2020.csv"

    df = get_formatted_df(path)[0]
    station_name = get_formatted_df(path)[1]
    year = '2020'
    filename=station_name+ '.html'
    start_html(station_name)

    PM25_LABEL = ('PM{}'.format(get_sub('2.5')))
    PM10_LABEL = ('PM{}'.format(get_sub('10')))
    NO2_LABEL = ('NO{}'.format(get_sub('2')))
    NOx_LABEL = ('NO{}'.format(get_sub('x')))
    SO2_LABEL = ('SO{}'.format(get_sub('2')))
    O3_LABEL = ('O{}'.format(get_sub('3')))

    local_df = df.copy(deep=True)
    local_df['date'] =  pd.to_datetime(local_df['dates'] ).dt.date

    #
    # try:
    #     local_df = get_clean_by_diff(local_df, 'PM25',PM25_LABEL,station_name, 1, 12)
    # except:
    #     print('error in PM25', station_name)
    #     pass
    #
    # try:
    #     local_df = get_clean_by_diff(local_df, 'PM10', PM10_LABEL,station_name,1, 12)
    # except:
    #     print('error in PM10', station_name)
    #     pass

    try:
        local_df =get_clean_by_diff(local_df, 'NOx', NOx_LABEL,station_name,1, 12)
    except:
        print('error in NOx', station_name)
        pass
    #
    # try:
    #     local_df = get_clean_by_diff(local_df, 'NO', 'NO',station_name,1, 12)
    # except:
    #     print('error in NO', station_name)
    #     pass
    # try:
    #     local_df = get_clean_by_diff(local_df, 'NO2', NO2_LABEL,station_name,1, 12)
    # except:
    #     print('error in NO2', station_name)
    #     pass
    #
    # try:
    #     local_df = get_clean_by_diff(local_df, 'SO2', SO2_LABEL,station_name,1, 12)
    # except:
    #     print('error in SO2', station_name)
    #     pass
    # try:
    #     local_df =  get_clean_by_diff(local_df, 'Ozone', O3_LABEL,station_name,1, 12)
    # except:
    #     print('error in Ozone', station_name)
    #     pass
    # local_df.to_csv(str(station_name) + ".csv")
    # print("Done with ", station_name)
