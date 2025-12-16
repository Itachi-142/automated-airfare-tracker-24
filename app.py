import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- PAGE SETUP ---
st.set_page_config(page_title="Flight Price Tracker", page_icon="✈️", layout="centered")

st.title("✈️ Real-Time Flight Price Intelligence")
st.write("Tracking flight prices dynamically to find the best time to buy.")

# --- DATA LOADER (With Caching for Speed) ---
def load_data():
    conn = sqlite3.connect('flight_prices.db')
    
    # Get Route Names
    routes = pd.read_sql_query("SELECT * FROM monitored_routes", conn)
    
    # Get Price History
    prices = pd.read_sql_query("SELECT * FROM flight_prices", conn)
    
    conn.close()
    
    # Merge them so we have City Names + Prices in one table
    # We join on 'route_id' from prices and 'id' from routes
    full_df = pd.merge(prices, routes, left_on='route_id', right_on='id')
    
    # Convert date column to correct time format
    full_df['scraped_at'] = pd.to_datetime(full_df['scraped_at'])
    return full_df

# Load the data
try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading database: {e}")
    st.stop()

if df.empty:
    st.warning("⚠️ No data found! Run 'scraper.py' to fetch prices first.")
    st.stop()

# --- SIDEBAR: ROUTE SELECTION ---
st.sidebar.header("🎯 Filter Options")

# Create a list of route names like "BLR -> DEL"
unique_routes = df.apply(lambda x: f"{x['source_city']} -> {x['destination_city']}", axis=1).unique()

selected_route = st.sidebar.selectbox("Select a Route to Analyze:", unique_routes)

# Filter data based on selection
# We split the string "BLR -> DEL" back into "BLR" and "DEL" to filter
source, dest = selected_route.split(" -> ")
filtered_df = df[(df['source_city'] == source) & (df['destination_city'] == dest)].sort_values('scraped_at')

# --- KPI METRICS ---
if not filtered_df.empty:
    latest_price = filtered_df.iloc[-1]['price']
    lowest_price = filtered_df['price'].min()
    highest_price = filtered_df['price'].max()

    # Create 3 columns for metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("📉 Lowest Price", f"₹{lowest_price:,.0f}")
    col2.metric("💰 Current Price", f"₹{latest_price:,.0f}")
    col3.metric("📈 Highest Price", f"₹{highest_price:,.0f}")

# --- GRAPH ---
st.subheader(f"Price Trend: {selected_route}")

fig, ax = plt.subplots(figsize=(10, 5))

# Plot the blue line
ax.plot(filtered_df['scraped_at'], filtered_df['price'], marker='o', linestyle='-', color='#0052cc', linewidth=2)

# Formatting
ax.set_title(f"History for {selected_route}", fontsize=12)
ax.set_ylabel("Price (INR)")
ax.grid(True, linestyle='--', alpha=0.5)

# Format Date Axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b %H:%M'))
fig.autofmt_xdate()

# Display Graph in Streamlit
st.pyplot(fig)

# --- RAW DATA TABLE ---
with st.expander("📊 View Raw Data"):
    st.dataframe(filtered_df[['scraped_at', 'airline', 'price']].sort_values('scraped_at', ascending=False))

# Refresh Button
if st.button('🔄 Refresh Data'):
    st.rerun()