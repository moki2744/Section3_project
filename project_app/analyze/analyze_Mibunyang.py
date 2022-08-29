import sqlite3
import pandas as pd

conn = sqlite3.connect('../section3_project4.db')
cur = conn.cursor()
query = cur.execute("""
SELECT m.City, m.Region, AVG(m.Num_mibunyang) AS Num_mibunyang
FROM Mibunyang m
WHERE m.Date > 202203
GROUP BY Region;
""")
cols = [column[0] for column in query.description]
query1 = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

query = cur.execute("""
SELECT h.City, h.Region, h.Num_households
FROM household2 h
WHERE h.Date > 202203
GROUP BY Region;
""")
cols = [column[0] for column in query.description]
query2 = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

conn.close()

query1['Num_mibunyang'] = query1.apply(lambda x : 0.1 if x.Num_mibunyang == 0 else x.Num_mibunyang, axis=1)
query2.Num_households = query2.Num_households.astype(float)
query_merge = pd.merge(query1, query2, how='left', on=['City','Region'])
query_merge['Mibunyang_rate'] = query_merge.apply(lambda x: (float(x.Num_mibunyang)/(x.Num_households * 0.003)), axis=1, )

# 지난 3개월 미분양수 평균 / 세대수 * 0.3 이 1이하인 경우 -> 오름차순으로 정리
query_merge[query_merge['Mibunyang_rate'] < 1].sort_values('Mibunyang_rate')
breakpoint()
