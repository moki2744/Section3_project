import requests
import sqlite3
import time
import json

query = f'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&format=json&jsonVD=Y&userStatsId=darksniper27/116/DT_MLTM_1946/2/1/20220824130014_1&prdSe=M&startPrdDe=200701&endPrdDe=202206'
r = requests.get(query)
data = r.json()

with open ("temp.json", "w") as f:
    f.dump((data, f))
