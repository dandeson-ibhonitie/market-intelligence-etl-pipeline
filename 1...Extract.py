import json
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# =====================================================================
# STAGE 1: EXTRACTION 
# =====================================================================
print(" Extracting Data...")

url = 'https://www.scrapethissite.com/pages/simple/'
ua = UserAgent()
custom_headers = {"User-Agent": ua.random}

response = requests.get(url, headers=custom_headers)
soup = BeautifulSoup(response.text, "html.parser")

all_countries_records = []
country_blocks = soup.find_all("div", class_="country")
print(f" Found {len(country_blocks)} raw layout blocks. Extracting text attributes...")

for block in country_blocks:
    name = block.find("h3", class_="country-name").text.strip()
    capital = block.find("span", class_="country-capital").text.strip()
    population = block.find("span", class_="country-population").text.strip()
    area = block.find("span", class_="country-area").text.strip()

    country_row = {
        "country_name": name,
        "capital_city": capital,
        "population": population,
        "area_sq_km": area,
    }
    all_countries_records.append(country_row)

# Save  to data lake landing zone
with open("raw_countries.json", "w", encoding="utf-8") as file:
    json.dump(all_countries_records, file, indent=4)

print(" Stage 1 Finished! Data extracted to 'raw_countries.json'.\n")

