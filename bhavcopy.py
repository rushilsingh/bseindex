import os
import requests
import io
import zipfile
import datetime

class BhavCopy(object):

    def __init__(self):
        self.base_url = "https://www.bseindia.com/download/BhavCopy/Equity/EQ{}_CSV.ZIP"
        self.base_fname = "EQ{}.CSV"
        self.redis_fname = "commands.txt"
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
        self.headers = self.text.split()[0].split(",")
        base_command = """ awk -F, 'BEGIN {OFS=","} %s' """ +  self.fname + """ | sed 's/\\"//g' > %s """ % self.redis_fname
        inner_command = "{print \"SET\"%s}"
        columns = ""
        for i in range(len(self.headers)):
            columns += ",$%s" % (i+1)

        inner_command = inner_command % columns
        command = base_command % inner_command
        os.system(command)

        os.unlink(self.fname)
        with open(self.redis_fname) as f:
            self.text = f.readlines()

        parsed_commands = ""
        for line in self.text:
            line = line.rstrip().rstrip(",")
            line = " ".join(line.split(","))
            parsed_commands += (line) + "\n"
        os.unlink(self.redis_fname)
        with open(self.redis_fname, "w") as f:
            f.write(parsed_commands)

        os.system("cat %s; sleep 5 | redis-cli --pipe" % self.redis_fname)
        os.unlink(self.redis_fname)


if __name__ == "__main__":
    bhavcopy = BhavCopy()
    bhavcopy.download()
    bhavcopy.parse()
