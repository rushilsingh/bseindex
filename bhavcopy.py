import requests
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
        print today
        print type(today)
        url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ"+today+"_CSV.ZIP"
        print url
        response = requests.get(url)
        print response

bhavcopy = BhavCopy()

