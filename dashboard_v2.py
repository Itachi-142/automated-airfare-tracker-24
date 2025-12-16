import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_route_name(route_id, conn):
    # Helper function to get "BLR -> DEL" from ID 1
    cursor = conn.cursor()
    cursor.execute("SELECT source_city, destination_city FROM monitored_routes WHERE id = ?", (route_id,))
    row = cursor.fetchone()
    if row:
        return f"{row[0]} -> {row[1]}"
    return f"Route {route_id}"

# 1. Load Data
conn = sqlite3.connect('flight_prices.db')
query = "SELECT * FROM flight_prices"
df = pd.read_sql_query(query, conn)

# 2. Setup the Graph
plt.figure(figsize=(12, 7))

# 3. Loop through each unique route in the data
# This effectively groups the data by route_id (1, 2, 3, 4)
route_ids = df['route_id'].unique()

print(f"📊 Found data for {len(route_ids)} routes. Plotting...")

for r_id in route_ids:
    # Filter data for ONLY this route
    route_data = df[df['route_id'] == r_id].copy()
    
    # Sort by date
    route_data['scraped_at'] = pd.to_datetime(route_data['scraped_at'])
    route_data = route_data.sort_values('scraped_at')
    
    # Get a nice name for the legend (e.g., "BOM -> DXB")
    label_name = get_route_name(r_id.item(), conn)
    
    # Plot this specific line
    plt.plot(route_data['scraped_at'], route_data['price'], marker='o', label=label_name)

conn.close()

# 4. Formatting
plt.title('Flight Price Tracker: Multi-City Analysis', fontsize=16)
plt.xlabel('Date of Check', fontsize=12)
plt.ylabel('Price (INR)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend() # Shows the box telling you which color is which city

# Format Dates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.gcf().autofmt_xdate()

print("✅ Dashboard updated. Opening graph...")
plt.tight_layout()
plt.show()