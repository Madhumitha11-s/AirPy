# AirPy

## Intructions to install AirPy:

1. Install the Python 3.7 version from `https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe`

2. Enter `cmd` in windows search and open the command prompt

3. Navigate to the working directory by entering `cd C:***\AirPy-main` in cmd

4. In cmd: <br />
    `pip install virtualenv` <br />
    `pip install --upgrade pip` <br />
    `virtualenv venv --python=python3.7` <br />
    `venv\Scripts\activate`     <br />
    `pip install -r "C:***\AirPy-main\requirements.txt"` <br />
    
5. To open AirPy <br />
    `jupyter notebook` or `python -m IPython notebook` <br />
  
## Input formats
Upload the pollutant data in `C:***\AirPy-main\Before_cleaning`
1. Excel: Unprocessed CPCB outputs (for one site containing multiple pollutant data and not  multiple site comparison data)
![image](https://user-images.githubusercontent.com/79834018/215360047-c1b3756d-5a3f-47e3-bc27-c0360762e5c2.png)

2. Processed csv files:
Name format:  site name_year.csv
![image](https://user-images.githubusercontent.com/79834018/215360150-07fd4d56-c7d1-4f7b-a09c-7efce28b8114.png)

## User specifications
Open Airpy.ipynb file and edit these specifications as required
*  year - enter the year of data you are interested in
*  path - airpy folder path
*  mixed_unit_identification - `False` for automating the unit correction, else `True`

## Outputs
*  cleaned pollutant data will be found with suffix "_clean" for all 6 pollutants and "_CPCB" denoting the cleaned and unit corrected versions of NO, NO2, NOx data in µg/m3, µg/m3 and ppb, respectively and  "_ppb" denoting all three pollutant data in ppb units
*  HTML file contains all timeseries and other information
*  

