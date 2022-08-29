import requests
import sqlite3
import time

key = 'ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM='
url = 'https://kosis.kr/openapi/statisticsList.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&vwCd=MT_ZTITLE&parentListId=A_7&format=json&jsonVD=Y'

conn = sqlite3.connect("./num_households.db")
cur = conn.cursor()

for i in range(1,91):
    query = f'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&format=json&jsonVD=Y&userStatsId=darksniper27/408/DT_408_2006_S0064/2/1/20220824145815_{i}&prdSe=M&startPrdDe=200601&endPrdDe=202206'
    r = requests.get(query)
    data = r.json()
    for i in range(len(data)):
        if len(data) <=3:
            continue
        else:
            cur.execute(f"""
                INSERT INTO Tradeamount VALUES ("{data[i]['C1']}", "{data[i]['C1_NM']}", "{data[i]['PRD_DE']}", "{data[i]['DT']}")
            """)
    time.sleep(0.3)
conn.commit()
conn.close()


