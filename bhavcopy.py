import os
import requests
import io
import zipfile
import datetime
import textfsm

class BhavCopy(object):

    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP"
        self.base_fname = "EQ{}.CSV"
        self.commands = "commands.txt"
        self.response = None
        self.timedelta = 0

    def download(self):

        while(self.response is None or self.response.status_code != 200):
            self.date_string = self.get_date_string()
            self.url = self.base_url.format(self.date_string)
            self.response = requests.get(self.url, stream=True)

            self.timedelta += 1
        self.timedelta = 0

        self.fname = self.base_fname.format(self.date_string)
        z = zipfile.ZipFile(io.BytesIO(self.response.content))
        z.extractall()
        with open(self.fname) as f:
            self.text = f.read()



    def get_date_string(self):

        stamp = datetime.datetime.today() - datetime.timedelta(days=self.timedelta)
        day = str(stamp.day) if len(str(stamp.day))==2 else (str(0) + str(stamp.day))
        month = str(stamp.month) if len(str(stamp.month))==2 else (str(0) + str(stamp.month))
        year = str(stamp.year)[-2:]
        year = year if len(year)==2 else (str(0)+year)
        return (day+month+year)

    def get_url(self):
        return self.base_url.format(self.date_string)

    def parse(self):
        template = "bhavcopy_template"

        with open(template) as f:
            parser = textfsm.TextFSM(f)

        lists = parser.ParseText(self.text)
        parsed = []
        for i in xrange(len(lists)):
            elem = {}
            for j in xrange(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)
       index = 1
       for record in parsed:
            for key in record:
                print(key +str(index) + " " +record[key])

                    



                

       

if __name__ == "__main__":
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()
