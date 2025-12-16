import schedule
import time
import subprocess
from datetime import datetime

print("------------------------------------------------")
print("🕒 Scheduler Started. I will run the scraper every 1 minute.")
print("------------------------------------------------")

def job():
    print(f"⏰ It is {datetime.now().strftime('%H:%M:%S')}. Waking up the scraper...")
    
    # This runs your existing scraper.py file
    try:
        subprocess.run(["python", "scraper.py"], check=True)
        print("✅ Scraper finished successfully.")
    except Exception as e:
        print(f"❌ Scraper crashed: {e}")
    
    print("------------------------------------------------")
    print("💤 Waiting for the next run...")

# SCHEDULE: Run every 1 minute for testing
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)