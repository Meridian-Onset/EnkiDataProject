import requests
import os
import time

filename = "download_links.txt"

'''
(Windows) When downloading from NASA Earthdata affiliated sites, don't forget to 
write a .netrc file in the following format:

 machine urs.earthdata.nasa.gov login <uid> password <password>

Check the site below for more info on how to access these files

 https://disc.gsfc.nasa.gov/data-access#python-requests
'''

#Change working directory to file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

def filenameExtract(url):
    #Extract data file name from URL
    return(url.split('/')[-1])

if __name__ == "__main__":

    #Check for the appropriate file, containing links for download
    if filename not in os.listdir():
       print("No file appropriately named and supplied with data download links")
       quit()

    #Check for receptacle folder
    if "Data" not in os.listdir():
        print("Data folder for download does not exist, creating one.")
        os.mkdir("Data")

    #Read the links into the program
    with open(filename, 'r') as link_doc:
        links = link_doc.read().splitlines()

    #Finally Download and store all the data
    i, time1, time2 = [0, time.perf_counter(), 0]
    for url in links:
        r = requests.get(url, allow_redirects = True)
        try:
            r.raise_for_status()
            f = open(f'./Data/{filenameExtract(url)}', 'wb')
            f.write(r.content)
            f.close()
            print(f"Succesfully Downloaded File {i}/{len(links)}", end = '\r'); i += 1
        except:
            print('requests.get() returned an error code ' + str(r.status_code))
    time2 = time.perf_counter()
    print(f"Succesfully completed download of listed files! \n Time Taken: {time2-time1}")