import os
import requests
import io
import zipfile
import datetime

class BhavCopy(object):
    
    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"
        self.url_postfix = "_CSV.ZIP"
        response = None
        timedelta = 0
        while(response is None or response.status_code != 200):
            self.date_string = self.get_date_string(timedelta)
            url = self.get_url()
            print(url)
            response = requests.get(url, stream=True)
            print(response.status_code)

            timedelta += 1
    
        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        with open("EQ"+self.date_string+".CSV") as f:
            text = f.read()
            
        os.unlink("EQ"+self.date_string+".CSV")
        print text

    def get_date_string(self, timedelta=0):
        
        now = datetime.datetime.today() - datetime.timedelta(days=timedelta)
        day = str(now.day) if len(str(now.day))==2 else (str(0) + str(now.day))
        month = str(now.month) if len(str(now.month))==2 else (str(0) + str(now.month))
        year = str(now.year)[-2:]
        year = year if len(year)==2 else (str(0)+year)
        return (day+month+year)
    
    def get_url(self):
        return self.base_url + self.date_string + self.url_postfix

bhavcopy = BhavCopy()

