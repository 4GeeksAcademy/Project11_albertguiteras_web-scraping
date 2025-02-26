### BeutifulSoup

import os
from bs4 import BeautifulSoup 
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

url = "https://companies-market-cap-copy.vercel.app/index.html"
respuesta = requests.get(url)

soup = BeautifulSoup(respuesta.text, 'html.parser')

element = soup.find_all("table", limit = 1)[0]
rows = element.find_all('tr')

data_Tesla = []

for e in rows[1:]:
    row_value = e.find_all("td")
    year = row_value[0].text.strip()
    income = row_value[1].text.strip()
    revenue = row_value[2].text.strip()
    data_Tesla.append([year, income, revenue])

ds = pd.DataFrame(data_Tesla, columns = ['Year', 'Revenue', 'Change'])

ds["Revenue"] = ds["Revenue"].astype(str)
ds["Revenue"] = ds["Revenue"].str.replace('$', '').str.replace('B', '')

ds = ds.drop('Change', axis = 1)
ds = ds.sort_values("Year", ascending = True)
ds['Revenue'] = ds['Revenue'].astype(float)

conn = sqlite3.connect("tesla_revenues.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ingresos (
    fecha TEXT,
    ingresos REAL
)
""")

for index, row in ds.iterrows():
    cursor.execute("INSERT INTO ingresos (fecha, ingresos) VALUES (?, ?)", (row["Year"], row["Revenue"]))

conn.commit()
conn.close()


plt.figure(figsize=(10, 6))
plt.plot(ds["Year"], ds["Revenue"], marker='o', label="Revenue")
plt.title("Ingresos anuales de Tesla")
plt.xlabel("Fecha")
plt.ylabel("Ingresos en billones(USD)")
plt.xticks(rotation=45)
plt.legend()

plt.savefig("revenue_plot2.png")
plt.show()