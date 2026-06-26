import duckdb

con = duckdb.connect('airbnb.duckdb')

con.execute("CREATE OR REPLACE TABLE bronze_hosts AS SELECT * FROM read_csv_auto('../data/raw/hosts.csv')")
con.execute("CREATE OR REPLACE TABLE bronze_reviews AS SELECT * FROM read_csv_auto('../data/raw/reviews.csv')")
con.execute("CREATE OR REPLACE TABLE bronze_full_moon AS SELECT * FROM read_csv_auto('../data/raw/seed_full_moon_dates.csv')")

# Adapter selon le format réel du fichier listings
try:
    con.execute("CREATE OR REPLACE TABLE bronze_listings AS SELECT * FROM read_json_auto('../data/raw/listings.json')")
except Exception:
    con.execute("CREATE OR REPLACE TABLE bronze_listings AS SELECT * FROM read_csv_auto('../data/raw/listings.json')")  
    
print("Tables Bronze créées :")
print(con.execute("SHOW TABLES").fetchall())
con.close()