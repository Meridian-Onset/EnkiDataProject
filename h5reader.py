##################################################################################

import h5py
import pandas as pd
import numpy as np
import os
import collections

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

dataPath = "./Data"

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
    col1, col2, col3, col4, col5, col6, col7, col8 = generalColumnSew(fileConnection).values()
    finalDF  = pd.DataFrame({'Latitude' : Latitude, 'Longitude' : Longitude,
                            'asr_obs' : col1, 'aerosol_frac' : col2,
                            'asr' : col3, 'cloud_aerosol_obs' : col4,
                            'cloud_frac' : col5, 'column_od' : col6,
                             'grnd_detect' : col7, 'tcod_obs' : col8})
    return(finalDF)

##################################################################################
##################################################################################

if __name__ == "__main__":
    exampleFile = fileParse(dataPath)[0]
    #print(exampleFile)
    #version, date, time = dateExtract(exampleFile)
    
    f = h5py.File(exampleFile, 'r')
    df = DFBuild(f)
    print(df['tcod_obs'].unique())
    #print(generalColumnSew(f).values())
    f.close()    
    finalname = '-'.join(dateExtract(exampleFile)[0:2])
    df.to_csv(f'{finalname}.csv')
##################################################################################