### Selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()),
    options = options
)

URL = "https://companies-market-cap-copy.vercel.app/index.html"
driver.get(URL)

growth_per_year = []

growth = driver.find_elements(By.TAG_NAME, "td")
for element in growth:
    growth_per_year.append(element.text)

data_list_of_lists = [growth_per_year[i:i+3] for i in range(0, len(growth_per_year), 3)]
filtered_data = data_list_of_lists[:16]

ds = pd.DataFrame(filtered_data, columns = ['Year', 'Revenue', 'Change'])

ds["Revenue"] = ds["Revenue"].astype(str)
ds["Revenue"] = ds["Revenue"].str.replace('$', '').str.replace('B', '')

ds = ds.drop('Change', axis = 1)
ds = ds.sort_values("Year", ascending = True)

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
plt.yticks()
plt.legend()

plt.savefig("revenue_plot.png")
plt.show()

