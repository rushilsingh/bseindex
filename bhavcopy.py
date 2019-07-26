import os
import requests
import io
import zipfile
import datetime

class BhavCopy(object):
    
    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"
        self.url_postfix = "_CSV.ZIP"
        self.date_string = self.get_date_string()
        print self.date_string
        
        url = self.get_url()
        response = requests.get(url, stream=True)
        
        # TODO:
        # If response is 404, get yesterday's file

        z = zipfile.ZipFile(io.BytesIO(response.content))
        z.extractall()
        with open("EQ"+self.date_string+".CSV") as f:
            text = f.read()
            
        os.unlink("EQ"+self.date_string+".CSV")
        print text

    def get_date_string(self):
        
        now = datetime.datetime.today()
        day = str(now.day) if len(str(now.day))==2 else (str(0) + str(now.day))
        month = str(now.month) if len(str(now.month))==2 else (str(0) + str(now.month))
        year = str(now.year)[-2:]
        year = year if len(year)==2 else (str(0)+year)
        return (day+month+year)
    
    def get_url(self):
        return self.base_url + self.date_string + self.url_postfix

bhavcopy = BhavCopy()

