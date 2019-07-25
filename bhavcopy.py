import os
import requests
import io
import zipfile
import datetime

class BhavCopy(object):
    
    def __init__(self):
        current = str(datetime.datetime.now())
        current = current.split()[0]
        current = current.split("-")
        day = current[2]
        month = current[1]
        year = current [0][2:]
        today = day+month+year
        url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"+today+"_CSV.ZIP"
        response = requests.get(url, stream=True)
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        with open("EQ"+today+".CSV") as f:
            text = f.read()
            
        os.unlink("EQ"+today+".CSV")
        print text


bhavcopy = BhavCopy()

