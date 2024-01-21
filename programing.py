import requests
from bs4 import BeautifulSoup
import sqlite3
import time

url = "https://www.data.jma.go.jp/stats/etrn/view/daily_s1.php?prec_no=46&block_no=47670&year=2023&month=12&day=&view="

r  = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
rows = soup.find_all('tr', class_='mtx')

rows = rows[3:]
data = []

for row in rows:
    weather = row.find_all('td')
    if len(weather) >= 1:
        date = weather[0].text.strip()
        temperature = weather[6].text.strip()
        data.append((date, temperature))

for date, temperature in data:
    print(f"{date}: {temperature}:")

db_name = 'weather.sqlite'

con = sqlite3.connect(db_name)
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS weathers(
                date TEXT,
                temperature REAL
                )''')

sql_insert = '''INSERT INTO weathers(
                date, temperature)
                VALUES (?, ?)'''

cur.executemany(sql_insert, data)

con.commit()

con.close()