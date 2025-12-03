import os
import requests
import json
import logging
import psycopg2
from datetime import datetime
from psycopg2.extras import Json

# -------------------------------
# Logging
# -------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# -------------------------------
# Environment Variables
# -------------------------------
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Support multiple symbols: AAPL,MSFT,GOOGL
SYMBOLS = os.getenv("STOCK_SYMBOLS", "AAPL").split(",")

DB_HOST = os.getenv("POSTGRES_HOST", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "stocks_db")
DB_USER = os.getenv("POSTGRES_USER", "stocks_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "stocks_pass")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# -------------------------------
# Fetch stock data from API
# -------------------------------
def fetch_stock_data(symbol):
    logging.info(f"Fetching data for {symbol}...")

    url = (
        f"https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "Time Series (5min)" not in data:
            raise ValueError("Unexpected API response structure")

        latest_timestamp = list(data["Time Series (5min)"].keys())[0]
        entry = data["Time Series (5min)"][latest_timestamp]

        logging.info(f"Data received for {symbol} at {latest_timestamp}")

        return {
            "symbol": symbol,
            "price": float(entry["4. close"]),
            "open_price": float(entry["1. open"]),
            "high_price": float(entry["2. high"]),
            "low_price": float(entry["3. low"]),
            "close_price": float(entry["4. close"]),
            "volume": int(entry["5. volume"]),
            "api_timestamp": datetime.strptime(latest_timestamp, "%Y-%m-%d %H:%M:%S"),
            "source": "alpha_vantage",
            "raw_json": data,
        }

    except Exception as e:
        logging.error(f"Error fetching stock data for {symbol}: {e}")
        return None

# -------------------------------
# Insert / Update PostgreSQL
# -------------------------------
def upsert_to_postgres(record):
    logging.info("Connecting to PostgreSQL...")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
    )
    cursor = conn.cursor()

    sql = """
    INSERT INTO stock_prices
    (symbol, price, open_price, high_price, low_price, close_price, volume, api_timestamp, source, raw_json)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON CONFLICT (symbol, api_timestamp)
    DO UPDATE SET
        price = EXCLUDED.price,
        open_price = EXCLUDED.open_price,
        high_price = EXCLUDED.high_price,
        low_price = EXCLUDED.low_price,
        close_price = EXCLUDED.close_price,
        volume = EXCLUDED.volume,
        fetched_at = now(),
        raw_json = EXCLUDED.raw_json;
    """

    try:
        cursor.execute(sql, (
            record["symbol"],
            record["price"],
            record["open_price"],
            record["high_price"],
            record["low_price"],
            record["close_price"],
            record["volume"],
            record["api_timestamp"],
            record["source"],
            Json(record["raw_json"]),
        ))
        conn.commit()
        logging.info(f"DB updated successfully for {record['symbol']}.")

    except Exception as e:
        logging.error(f"DB insert/update failed for {record['symbol']}: {e}")
    finally:
        cursor.close()
        conn.close()

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    for symbol in SYMBOLS:
        symbol = symbol.strip()
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            upsert_to_postgres(stock_data)
        else:
            logging.error(f"No data fetched for {symbol}; skipping.")
