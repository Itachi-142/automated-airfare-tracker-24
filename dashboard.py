import sqlite3
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates

conn = sqlite3.connect('flight_prices.db')
query = "SELECT * FROM flight_prices"
df = pd.read_sql_query(query, conn)
conn.close()

if df.empty:
    print("No Data found! Please run scraper.py first")
else:
    print("Data loaded successfully. Here are the latest rows:")
    print(df[['scraped_at', 'price']].tail())
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    df = df.sort_values('scraped_at')
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['scraped_at'], df['price'], marker='o',linestyle='-',color='#1f77b4',linewidth=2)
    plt.title('Flight Price Trend: Bangalore (BLR) -> Delhi (DEL)', fontsize=14)
    plt.xlabel('Date & Time of Check', fontsize=12)
    plt.ylabel('Price (₹)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Format the Date on X-Axis to look nice
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gcf().autofmt_xdate() # Rotate dates so they don't overlap
    
    # Show the plot
    print("📊 Opening Graph Window...")
    plt.tight_layout()
    plt.show()