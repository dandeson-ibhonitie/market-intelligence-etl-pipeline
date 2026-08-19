# market-intelligence-etl-pipeline
A modular Python ETL pipeline demonstrating production best practices: web scraping with randomized user-agents, robust data cleaning/type casting via Pandas, and strict schema modeling using explicit SQL DDL.
# Simple Web Scraper to SQL Database (ETL Pipeline)

##  Why I Built This
When retail companies want to expand to new countries, they need to know which areas are already crowded and which ones have room to grow. Copying and pasting this data by hand from the web takes too long and it's easy to make mistakes. 

I built this project to automate the whole process. It's a 3-stage data pipeline that automatically grabs country details from a website, cleans up the messy formatting, calculates population density for each country, and saves everything into a local SQL database so anyone can query it easily.

---

## Tools Used & How Data Flows

```text
[ Website ] ──► [ extract.py ] ──► [ raw_countries.json ]
                                          │
                                          ▼
[ cleaned_countries.csv ] ◄── [ transform.py ]
            │
            ▼
     [ load.py ] ──► [ world_intelligence.db (SQLite3) ]
```

*   **Extract:** Python `requests` and `BeautifulSoup4` to scrape the webpage.
*   **Transform:** `Pandas` to clean the numbers and do calculations.
*   **Load:** `SQLite3` to store the clean data in structured tables.

---

##  How the Code is Organized

Instead of writing one giant script, I broke the project down into three smaller files to keep things clean and modular (just like in a real development environment):

*   **`extract.py`**: This script connects to the country directory website. It uses a random user-agent so the connection looks like a regular browser visit. It pulls out the raw text for country names, capitals, populations, and areas, then saves a raw backup file called `raw_countries.json`.
*   **`transform.py`**: This script handles the data cleaning. Web data usually loads as text strings with commas (like `"71,566"`), which means you can't do math on it. I used Pandas to remove the commas, convert the columns into integers and floats, and filter out any broken rows. Then, I calculated a new column (`population_density`) and saved the clean data to `cleaned_countries.csv`.
*   **`load.py`**: This script sets up the local database (`world_intelligence.db`). I wrote an explicit SQL query to create the table structure with proper data types and a Primary Key so we don't accidentally get duplicate data. Then, it loads the clean CSV data into the table and runs a quick SQL test query to print out the top results.

---

##  Sample Database Output

When you run the final loading script, it queries the database and prints out a quick report showing the top 5 most crowded markets:

```text
 Ingestion Complete! Data successfully loaded into 'world_intelligence.db'.

 --- STRATEGY ANALYTICS REPORT: TOP 5 MARKET DENSITIES ---
Country              | Capital              | Density (Pop/Sq Km)
--------------------------------------------------------------------
Macau                | Macau                | 21,114.67
Monaco               | Monaco               | 17,914.21
Singapore            | Singapore            | 7,208.56
Hong Kong            | Hong Kong            | 6,480.22
Gibraltar            | Gibraltar            | 4,521.15

 Connection closed securely. End-to-end pipeline finished!
```

---

##  How to Run and Test it Locally

1. Clone this repository to your machine:
   ```bash
   git clone https://github.com
   cd market-intelligence-etl-pipeline
   ```

2. Install the Python packages:
   ```bash
   pip install requests beautifulsoup4 pandas fake-useragent
   ```

3. Run the scripts in order:
   ```bash
   python extract.py
   python transform.py
   python load.py
   ```
