import logging
import sqlite3
import time
from datetime import datetime, timedelta

# --- IMPORTS FOR SELENIUM ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
# We will look for flights 60 days from today
flight_date = datetime.now() + timedelta(days=60)
DATE_STR = flight_date.strftime("%Y-%m-%d") 

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def get_db_connection():
    return sqlite3.connect('flight_prices.db')

def save_price(route_id, airline, price_text):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Clean the price text (remove ₹ and commas)
        clean_price = float(price_text.replace('₹', '').replace(',', ''))
        
        # ✅ FIX 1: Format the date as a string to avoid DeprecationWarning
        current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
        INSERT INTO flight_prices (route_id, airline, price, scraped_at)
        VALUES (?, ?, ?, ?)
        """, (route_id, airline, clean_price, current_time_str))
        
        conn.commit()
        logging.info(f"   ✅ Saved ₹{clean_price}")
    except Exception as e:
        logging.error(f"   ❌ Database Error: {e}")
    finally:
        conn.close()

# --- DRIVER SETUP ---
options = webdriver.ChromeOptions()
HEADLESS_MODE = True 

if HEADLESS_MODE:
    options.add_argument("--headless=new") 
    options.add_argument("--window-size=1920,1080")

options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- GET ROUTES ---
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT id, source_city, destination_city FROM monitored_routes")
routes = cursor.fetchall()
conn.close()

logging.info(f"🚀 Starting scrape for {len(routes)} routes on date: {DATE_STR}")

# --- THE LOOP ---
for route in routes:
    route_id = route[0]
    source = route[1]
    dest = route[2]
    
    logging.info(f"\n--- Checking {source} -> {dest} ---")
    
    # ✅ IMPROVED URL: Uses standard Google Flights search query
    url = f"https://www.google.com/travel/flights?q=Flights%20to%20{dest}%20from%20{source}%20on%20{DATE_STR}%20oneway"
    
    driver.get(url)
    
    # ✅ FIX 2: Removed time.sleep(6). Used Smart Wait.
    try:
        # Wait up to 15 seconds for the price to appear
        price_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "₹")]'))
        )
        
        price_text = price_element.text
        logging.info(f"   💰 Found: {price_text}")
        
        save_price(route_id, "Best Available", price_text)
        
    except TimeoutException:
        logging.warning("   ⚠️ Timed out! Price didn't load in 15 seconds.")
    except Exception as e:
        logging.error(f"   ❌ Error: {e}")

logging.info("\n🏁 All routes checked.")
driver.quit()