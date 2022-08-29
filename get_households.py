import requests
import sqlite3
import time

key = 'ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM='
url = 'https://kosis.kr/openapi/statisticsList.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&vwCd=MT_ZTITLE&parentListId=A_7&format=json&jsonVD=Y'
giguan_code = 101
table_ID = 'DT_1B040B3'

conn = sqlite3.connect("./num_households.db")
cur = conn.cursor()

City = 'Jejusi'
for i in range(1, 6):
    query = f'https://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=ZmQwODhjMzQ5ZTU1NjFmNzJhMmU3MzExN2I1ZjYzZmM=&format=json&jsonVD=Y&userStatsId=darksniper27/101/DT_1B040B3/2/1/20220822223849_{i}&prdSe=M&startPrdDe=201101&endPrdDe=202207'
    r = requests.get(query)
    data = r.json()
    for i in range(len(data)):
        if len(data) <=3:
            continue
        else:
            cur.execute(f"""
                INSERT INTO Household VALUES ("{City}", "{data[i]['C1_NM']}", "{data[i]['C1']}", "{data[i]['PRD_DE']}", "{data[i]['DT']}")
            """)
    time.sleep(0.3)
conn.commit()
conn.close()

