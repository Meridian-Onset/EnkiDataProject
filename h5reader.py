##################################################################################

import h5py
import pandas as pd
import numpy as np
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

dataPath = "./Data"

months = {'01' : 'Jan','02' : 'Feb', '03' : 'Mar', '04' : 'Apr',
          '05' : 'May', '06' : 'Jun', '07' : 'Jul', '08' : 'Aug', 
          '09' : 'Sep', '10' : 'Oct' ,'11' : 'Nov', '12' : 'Dec'}

##################################################################################

def fileParse(dirpath = dataPath):
    # Return a list of the absolute paths of the data files in given directory
    files = []
    for f in os.listdir(dataPath):
        files.append(dataPath + '/' + str(f))
    return(files)

def dateExtract(filePath):
    # Function for extracting the date, time and data version from the filepath
    name = filePath.split('/')[2]
    version = name.split('_')[0]
    #print(name.split())
    datetime = name.split('_')[1]

    date, time = datetime[0:8], datetime[8:16]
    date = date[6:8] + '-' + date[4:6] + '-' + date[:4]
    time = time[:2] + ':' + time[2:4] + ':' + time[4:6]

    return(version, date, time)

def locationData(fileConnection):
    # Return two single dimension arrays of all combinations of the coordinate data,
    # column-wise bound
    locationTags = ['global_grid_lat', 'global_grid_lon']
    
    lat = np.array(fileConnection[locationTags[0]])
    lon = np.array(fileConnection[locationTags[1]])
    dataLon = np.empty(len(lat)*len(lon))
    dataLat = np.empty(len(lat)*len(lon))
    i = 0
    for longitude in lon:
        for latitude in lat:
            dataLon[i] = longitude
            dataLat[i] = latitude
            i += 1 
    
    return(dataLat, dataLon)

def globalKeysFinder(fileConnection, coordShape = (90,180)):
    #Find Keys corresponding to shapes of different coordinate systems,
    # default is the global coordinates, other shape is (15,180) for npolar and 
    # spolar coordinates
    for Key in list(fileConnection.keys()):
        try:
            if fileConnection[Key].shape == coordShape:
                print(Key)
            else: pass
        except AttributeError: pass

def generalColumnSew(fileConnection):
    # Determine compatible keys using above globalKeyFinder function
    returnArrays = dict({'asr_obs_grid' : np.empty([16200]),
                        'global_aerosol_frac' : np.empty([16200]),
                        'global_asr' : np.empty([16200]), 
                        'global_cloud_aerosol_obs_grid' : np.empty([16200]),
                        'global_cloud_frac' : np.empty([16200]),
                        'global_column_od' : np.empty([16200]), 
                        'global_grnd_detect' : np.empty([16200]), 
                        'tcod_obs_grid' : np.empty([16200])})
    for Key, KeyArray in returnArrays.items():
        i = 0
        for item in np.array(fileConnection[Key]).flatten():
            KeyArray[i] = item
            i += 1
    return(returnArrays)

def DFBuild(fileConnection):
    Latitude, Longitude = locationData(fileConnection)
    #print(fileConnection.filename)
    month = dateExtract(fileConnection.filename)[1]
    
    col1, col2, col3, col4, col5, col6, col7, col8 = generalColumnSew(fileConnection).values()
    finalDF  = pd.DataFrame({'GranuleID' : range(1,len(Latitude)+1),
                             'MON' : [months[month[3:5]]] * len(Latitude),
                             'Latitude' : Latitude, 'Longitude' : Longitude,
                             'asr_obs' : col1, 'aerosol_frac' : col2,
                             'asr' : col3, 
                             'cloud_aerosol_obs' : col4, 'cloud_frac' : col5,
                             'column_od' : col6, 'grnd_detect' : col7,
                             'tcod_obs' : col8})
    return(finalDF)

##################################################################################
##################################################################################

if __name__ == "__main__":

    
    datedata = dict()
    df2018 = pd.DataFrame(columns = ['GranuleID', 'MON', 
                                                 'Latitude', 'Longitude',
                                                 'asr_obs', 'aerosol_frac',
                                                 'asr', 'cloud_aerosol_obs',
                                                 'cloud_frac', 'column_od',
                                                 'grnd_detect', 'tcod_obs'])
    df2019, df2020 = df2018.copy(), df2018.copy()
    for file in fileParse('.\Data'):
        
        version, year, time = dateExtract(file)
        month = year[3:5]
        year = year[8:10]
        
        
        
        if year not in datedata.keys():
            datedata[year] = []
            
        if month not in datedata[year]:
            datedata[year].append(months[month])
            
            f = h5py.File(file, 'r')
            df = DFBuild(f)
            f.close()
            if year == '18':  df2018 = df2018.append(df)
            elif year == '19': df2019 = df2019.append(df)
            elif year == '20': df2020 = df2020.append(df)
            else: print("Funky data year")
        else: pass

    df2018.to_csv('ATL16_2018.csv')
    df2019.to_csv('ATL16_2019.csv')
    df2020.to_csv('ATL16_2020.csv')
##################################################################################