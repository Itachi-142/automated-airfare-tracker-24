from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import sqlite3
from datetime import datetime, timedelta

# --- CONFIGURATION ---
# We will look for flights 60 days from today
flight_date = datetime.now() + timedelta(days=60)
# Format date as YYYY-MM-DD for the URL (e.g., 2025-02-20)
DATE_STR = flight_date.strftime("%Y-%m-%d") 

def get_db_connection():
    return sqlite3.connect('flight_prices.db')

def save_price(route_id, airline, price_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        clean_price = float(price_text.replace('₹', '').replace(',', ''))
        cursor.execute("""
        INSERT INTO flight_prices (route_id, airline, price, scraped_at)
        VALUES (?, ?, ?, ?)
        """, (route_id, airline, clean_price, datetime.now()))
        conn.commit()
        print(f"   ✅ Saved ₹{clean_price}")
    except Exception as e:
        print(f"   ❌ Database Error: {e}")
    finally:
        conn.close()

# 1. Setup Driver
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 2. Get All Routes from DB
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, source_city, destination_city FROM monitored_routes")
routes = cursor.fetchall() # Returns a list like [(1, 'BLR', 'DEL'), (2, 'BOM', 'DXB')]
conn.close()

print(f"🚀 Starting scrape for {len(routes)} routes on date: {DATE_STR}")

# 3. The Loop
for route in routes:
    route_id = route[0]
    source = route[1]
    dest = route[2]
    
    print(f"\n--- Checking {source} -> {dest} ---")
    
    # Construct the Dynamic URL
    # This is the magic link that works for any city pair
    url = f"https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{source}%20on%20{DATE_STR}%20one-way"
    
    driver.get(url)
    time.sleep(6) # Wait for load
    
    try:
        # Find Price
        price_element = driver.find_element(By.XPATH, '//span[contains(text(), "₹")]')
        price_text = price_element.text
        print(f"   💰 Found: {price_text}")
        
        save_price(route_id, "Best Available", price_text)
        
    except Exception as e:
        print("   ⚠️ Price not found (Route might be invalid or blocked)")

print("\n🏁 All routes checked.")
driver.quit()