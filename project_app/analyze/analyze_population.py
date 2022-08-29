import sqlite3
import pandas as pd

conn = sqlite3.connect('../section3_project4.db')
cur = conn.cursor()
query = cur.execute("""
SELECT p.City, p.Region , SUM(p."2015") AS '2015', SUM(p."2016") AS '2016', SUM(p."2017") AS '2017', SUM(p."2018") AS '2018', SUM(p."2019") AS '2019', SUM(p."2020") AS '2020', SUM(p."2021") AS '2021'  
FROM Population_3050 p
GROUP BY City, Region;
""")
cols = [column[0] for column in query.description]
query1 = pd.DataFrame.from_records(data = query.fetchall(), columns=cols)

