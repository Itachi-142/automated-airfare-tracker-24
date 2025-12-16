import sqlite3
conn = sqlite3.connect('flight_prices.db')
cursor = conn.cursor()

route_table_query = """
CREATE TABLE IF NOT EXISTS
monitored_routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_city TEXT NOT NULL,
    destination_city TEXT NOT NULL,
    created_at TIMESTAMP DEFAULTCURRENT_TIMESTAMP
    );"""
    
prices_table_query = """
CREATE TABLE IF NOT EXISTS
flight_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route_id INTEGER,
    airline TEXT,
    flight_code TEXT,
    departure_time DATETIME,
    price REAL,
    scraped_at DATETIME,
    FOREIGN KEY (route_id) REFERENCES monitored_routes (id)
    );"""
    
print("Creating tables...")
cursor.execute(route_table_query)
cursor.execute(prices_table_query)

print("Adding 'BLR' to 'DEL' route...")
cursor.execute("""INSERT INTO monitored_routes (source_city, destination_city) SELECT 'BLR', 'DEL'
               WHERE NOT EXISTS (SELECT 1 FROM monitored_routes WHERE source_city = 'BLR' AND destination_city = 'DEL');""")

conn.commit()
conn.close()
print("Success! Database 'flight_prices.db' created")