# ✈️ Flight Price Intelligence System

An end-to-end data engineering pipeline that tracks flight prices, stores historical data, and helps users identify the optimal time to buy tickets.

## 📌 Overview
This project solves the problem of volatile flight pricing. Instead of manually checking prices every day, this system:
1.  **Automates** data collection using a Selenium bot.
2.  **Stores** price history in a structured SQL database.
3.  **Visualizes** trends via an interactive Streamlit dashboard.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Automation:** Selenium WebDriver (Web Scraping)
* **Database:** SQLite3 (Relational Data Storage)
* **Visualization:** Streamlit & Matplotlib
* **Scheduling:** Python `schedule` library

## 📂 Project Structure
* `scraper.py`: The "Worker" bot that scrapes Google Flights.
* `scheduler.py`: The "Manager" that runs the scraper every 6 hours.
* `app.py`: The "Frontend" dashboard for data visualization.
* `flight_prices.db`: The "Memory" (SQL Database).
* `setup_database.py`: Utility to initialize the database schema.

## 🚀 How to Run Locally

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/flight-price-tracker.git](https://github.com/YOUR_USERNAME/flight-price-tracker.git)
    cd flight-price-tracker
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the Scheduler (Data Collection)**
    ```bash
    python scheduler.py
    ```

4.  **Launch the Dashboard (Visualization)**
    ```bash
    streamlit run app.py
    ```

## 📊 Features
* **Dynamic URL Generation:** Automatically generates links for any city pair (e.g., BLR → DEL, BOM → DXB).
* **Anti-Bot Detection:** Uses human-like delays and browser mimicry.
* **Data Persistence:** Saves data permanently to SQLite, avoiding data loss on shutdown.
* **Interactive Analytics:** Filter by route, view lowest/highest prices, and track trends over time.

---
*Built as a Data Engineering Portfolio Project.*