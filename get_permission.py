import requests
import sqlite3
import time

key = 'ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM='
url = 'https://kosis.kr/openapi/statisticsList.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&vwCd=MT_ZTITLE&parentListId=A_7&format=json&jsonVD=Y'

conn = sqlite3.connect("./num_households.db")
cur = conn.cursor()

for i in range(1, 18):
    query = f'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&format=json&jsonVD=Y&userStatsId=darksniper27/116/DT_MLTM_1946/2/1/20220824130014_{i}&prdSe=M&startPrdDe=200701&endPrdDe=202206'
    r = requests.get(query)
    data = r.json()
    for i in range(len(data)):
        if len(data) <=3:
            continue
        else:
            cur.execute(f"""
                INSERT INTO Permission VALUES ("{data[i]['C3_NM']}", {data[i]['PRD_DE']}, {data[i]['DT']})
            """)
    time.sleep(0.3)
conn.commit()
conn.close()

