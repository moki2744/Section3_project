import sqlite3
import pandas as pd

conn = sqlite3.connect('section3_project3.db')
cur = conn.cursor()
query = cur.execute("""
SELECT t.City_hint, t.Region, AVG(Num_trade) AS Average
FROM Tradeamount2 t
WHERE t.Date > 202007
GROUP BY t.City_hint, t.Region;
""")
cols = [column[0] for column in query.description]
query1 = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

query = cur.execute("""
SELECT t2.City_hint, t2.Region, t2.Num_trade AS 'Recent_result' 
FROM Tradeamount2 t2 
WHERE t2.Date == 202206
ORDER BY Region ;
""")
cols = [column[0] for column in query.description]
query2 = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

conn.close()

query_merge = pd.merge(query1, query2, how='left', on=['City_hint','Region'])
query_merge['trade_rate'] = query_merge.apply(lambda x: (float(x.Recent_result)/float(x.Average)), axis=1, )

# 이번달 거래량 / 지난 2년 6개월의 거래량 이 1이상인 경우 -> 내림차순으로 정리
query_merge[query_merge['trade_rate'] > 1].sort_values('trade_rate', ascending=False)