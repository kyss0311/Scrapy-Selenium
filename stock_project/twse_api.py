import requests as rq

res = rq.get("https://openapi.twse.com.tw/v1/exchangeReport/BWIBBU_ALL")
info = res.json()[0]
print("Name: ", info['Name'])
print("PBratio: ", info['PBratio'])
