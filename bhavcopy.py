import requests

response = requests.get("https://www.bseindia.com/download/BhavCopy/Equity/EQ250719_CSV.ZIP")
print(dir(response))
