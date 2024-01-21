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