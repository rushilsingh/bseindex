import os
import requests
import io
import zipfile
import datetime
import textfsm
import redis
import pytz


class BhavCopy(object):

    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP"
        self.base_fname = "EQ{}.CSV"
        self.response = None
        self.timedelta = 0
        self.fname = None

    def download(self):

        while(self.response is None or self.response.status_code != 200):
            self.date_string = self.get_date_string()
            self.url = self.base_url.format(self.date_string)
            self.response = requests.get(self.url, stream=True)

            self.timedelta += 1
        self.timedelta = 0

        fname = self.base_fname.format(self.date_string)
        if self.fname != fname:
            self.fname = fname
            z = zipfile.ZipFile(io.BytesIO(self.response.content))
            z.extractall()
            with open(self.fname) as f:
                self.text = f.read()
            os.unlink(self.fname)
            self.parse()


    def get_date_string(self):

        stamp = datetime.datetime.now(pytz.timezone("Asia/Kolkata")) - datetime.timedelta(days=self.timedelta)
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
        for i in range(len(lists)):
            elem = {}
            for j in range(len(parser.header)):
                elem[parser.header[j]] = lists[i][j]
            parsed.append(elem)
        index = 1

        red = redis.from_url(os.environ.get('REDIS_URL'), decode_responses=True)
        red.flushdb()
        pipe = red.pipeline()
        n = 1
        diffs = []
        for record in parsed:
            name = record["Name"]
            open_value = float(record["Open"]
            close_value = float(record["Close"])
            diff = open_value - close_value
            diff = (diff/open_index) * 100.00000
            name = "\"" + name + "\"" if " " in name else name
            from copy import deepcopy
            input_values = deepcopy(record)
            input_values.extend({"Change": diff})
            diffs.append(diff)
            pipe.hset("Names", name, record)
            pipe.hset("Diffs", str(diff), record)
        diffs.sort()
        if len(diffs)>10:
            diffs = diffs[:10]
        self.top = diffs

if __name__ == "__main__":
    bhavcopy = BhavCopy()
    bhavcopy.download()
