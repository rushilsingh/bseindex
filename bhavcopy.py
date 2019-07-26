import os
import requests
import io
import zipfile
import datetime

class BhavCopy(object):
    
    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP"
        self.base_fname = "EQ{}.CSV" 
        response = None
        timedelta = 0
        while(response is None or response.status_code != 200):
            self.date_string = self.get_date_string(timedelta)
            self.url = self.base_url.format(self.date_string)
            print(self.url)
            response = requests.get(self.url, stream=True)
            print(response.status_code)

            timedelta += 1
        self.fname = self.base_fname.format(self.date_string)
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        with open(self.fname) as f:
            self.text = f.read()
            
        os.unlink(self.fname)
        

    def get_date_string(self, timedelta=0):
        
        now = datetime.datetime.today() - datetime.timedelta(days=timedelta)
        day = str(now.day) if len(str(now.day))==2 else (str(0) + str(now.day))
        month = str(now.month) if len(str(now.month))==2 else (str(0) + str(now.month))
        year = str(now.year)[-2:]
        year = year if len(year)==2 else (str(0)+year)
        return (day+month+year)
    
    def get_url(self):
        return self.base_url.format(self.date_string)

bhavcopy = BhavCopy()
print(bhavcopy.text)

