# =====================================================================
# STAGE 3: LOADING & ANALYTICS (load.py module)
# =====================================================================
print("Loading the Data to warehouse")

# Ingest from staging lake layer
df_clean = pd.read_csv("cleaned_countries.csv")

# Open production database connection network session
conn = sqlite3.connect("world_intelligence.db")
cursor = conn.cursor()

# Enforce strict  relational schemas via DDL execution
create_table_query = """
CREATE TABLE IF NOT EXISTS countries (
    country_name TEXT PRIMARY KEY,
    capital_city TEXT,
    population INTEGER,
    area_sq_km REAL,
    population_density REAL
);
"""
cursor.execute(create_table_query)
conn.commit()

# Bulk stream records into SQL table interface
df_clean.to_sql("countries", con=conn, if_exists="replace", index=False)


# Production query validation audit
verification_query = """
SELECT country_name, capital_city, population, area_sq_km, population_density 
FROM countries 
ORDER BY population_density DESC 
LIMIT 5;
"""
cursor.execute(verification_query)
top_5_countries = cursor.fetchall()

print("\n --- STRATEGY ANALYTICS REPORT: TOP 5 MARKET DENSITIES ---")
print(f"{'Country':<20} | {'Capital':<20} | {'Density (Pop/Sq Km)':<20}")
print("=" * 68)
for row in top_5_countries:
    print(f"{row[0]:<20} | {row[1]:<20} | {row[4]:<20,.2f}")

# Closing Database
conn.close()
print("\n Connection closed securely. ")