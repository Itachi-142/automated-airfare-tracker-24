import sqlite3

conn = sqlite3.connect('flight_prices.db')
cursor = conn.cursor()

# List of new routes to add (Source, Destination)
# You can change these to whatever cities you want!
new_routes = [
    ('BOM', 'DXB'),  # Mumbai -> Dubai
    ('DEL', 'LHR'),  # Delhi -> London
    ('MAA', 'SIN')   # Chennai -> Singapore
]

print("Adding new routes...")
for source, dest in new_routes:
    # We use 'INSERT OR IGNORE' so we don't add duplicates if you run this twice
    cursor.execute("""
        INSERT INTO monitored_routes (source_city, destination_city)
        SELECT ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM monitored_routes 
            WHERE source_city = ? AND destination_city = ?
        )
    """, (source, dest, source, dest))

conn.commit()
print(f"✅ Added {len(new_routes)} new routes to the database.")
conn.close()