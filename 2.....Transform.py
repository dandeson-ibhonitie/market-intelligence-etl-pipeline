# =====================================================================
# STAGE 2: TRANSFORMATION 
# =====================================================================
print(" Transforming Data ...")

# Reading  from raw storage 
df2 = pd.read_json("raw_countries.json")


# Cleaning missing values
df2["capital_city"] = df2["capital_city"].fillna("Unknown")
df2["capital_city"] = df2["capital_city"].replace("", "Unknown")

# making sure of numeric float
df2["population"] = df2["population"].astype(int)
df2["area_sq_km"] = df2["area_sq_km"].astype(float)

# Filtering out zero values
df2 = df2[(df2["population"] > 0) & (df2["area_sq_km"] > 0)]

# Creating a new column (KPI)
df2["population_density"] = df2["population"] / df2["area_sq_km"]

# Export verified dataset to staging lake layer
df2.to_csv("cleaned_countries.csv", index=False)
print(" Cleaned dataset exported to 'cleaned_countries.csv'.\n")
