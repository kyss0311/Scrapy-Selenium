import requests as rq
import re

proxy_url = "https://free-proxy-list.net/"
api_url = "https://www.ipify.org/?format=json"

res = rq.get(proxy_url)

pattern = "\d+\.\d+\.\d+\.\d+:\d+"
proxies = re.findall(pattern, res.text)

for proxy in proxies:
    try:
        res = rq.get(api_url, proxies={
            "http": proxy,
            "https": proxy
        }, timeout=5)
        print(res.json())
    except:
        print(f"Invalid{proxy}")
