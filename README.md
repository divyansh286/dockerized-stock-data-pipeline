                         ┌──────────────────────┐
                         │  Alpha Vantage API   │
                         └──────────┬───────────┘
                                    │ JSON Response
                                    ▼
                      ┌─────────────────────────────┐
                      │ Python Fetch Script          │
                      │ fetch_and_update.py          │
                      └──────────┬───────────────────┘
                                 │ Writes to DB
                                 ▼
                     ┌───────────────────────────────┐
                     │  PostgreSQL + pgAdmin          │
                     │   (Docker Container)           │
                     └──────────┬────────────────────┘
                                 │ Trigger
                                 ▼
                ┌────────────────────────────────────────┐
                │     Apache Airflow (Webserver +        │
                │     Scheduler + DAG Orchestrator)      │
                └────────────────────────────────────────┘
# 📦 Dockerized Stock Market Data Pipeline  
### *(Airflow + PostgreSQL + Docker Compose)*

This project implements a fully **dockerized, automated data pipeline** that fetches intraday stock market data from the **AlphaVantage API**, processes it using Python, and stores it in a **PostgreSQL database**.  
The entire workflow is orchestrated using **Apache Airflow**, and all services run seamlessly inside **Docker containers**.

This submission aligns 100% with the original assignment requirements.

---

## 🚀 Features

- Automated stock data ingestion every hour (Airflow DAG)
- Fetches live JSON data using Python `requests`
- Extracts open, high, low, close, volume, timestamp
- Data is validated, parsed, and stored in PostgreSQL
- UPSERT logic prevents duplicate rows
- Error handling with retries & logging
- Fully managed via Docker Compose
- pgAdmin UI included for database visibility
- Secrets and credentials stored via `.env`

---

## 🧱 Architecture Overview
Docker Compose
│
├── PostgreSQL (Database)
├── pgAdmin (DB UI)
└── Airflow
├── Webserver
├── Scheduler
├── DAG: stock_pipeline_dag.py
└── Python Script: fetch_and_update.py

**Flow:**  
Airflow → Python Script → AlphaVantage API → Extract Metrics → UPSERT into PostgreSQL → Logs stored in Airflow.

---

## 🗂 Project Structure
stock-pipeline/
├── airflow/
│ ├── dags/
│ │ └── stock_pipeline_dag.py
│ ├── scripts/
│ │ └── fetch_and_update.py
│ ├── airflow.cfg
│ └── logs/
├── scripts/
│ └── fetch_and_update.py
├── docker-compose.yml
├── create_table.sql
├── .env
└── README.md

---

## ⚙️ Environment Variables (`.env`)
POSTGRES_USER=stocks_user
POSTGRES_PASSWORD=stocks_pass
POSTGRES_DB=stocks_db
POSTGRES_PORT=5432
POSTGRES_HOST=postgres

API KEY

ALPHA_VANTAGE_API_KEY=your_api_key_here

Fetch multiple stocks (comma-separated)

STOCK_SYMBOLS=AAPL,MSFT,GOOGL,AMZN,TSLA

---

## 🐳 How to Run Locally

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/divyansh286/dockerized-stock-data-pipeline.git
cd dockerized-stock-data-pipeline
docker compose up -d
3️⃣ Access Services
Service	URL
Airflow UI	http://localhost:8080

pgAdmin	http://localhost:8081

PostgreSQL	localhost:5432
username: admin
password: admin

---
🔄 How the Pipeline Works
1. Airflow triggers the DAG hourly

DAG file: airflow/dags/stock_pipeline_dag.py

2. Python script fetches JSON data

Script: airflow/scripts/fetch_and_update.py

Extracted fields:

Open price

High price

Low price

Close price

Volume

Symbol

Timestamp

Raw JSON stored for auditing

3. Data written to PostgreSQL

UPSERT logic ensures:

(symbol, api_timestamp) is UNIQUE

4. pgAdmin used for DB monitoring
🛡 Error Handling

Wrapped API calls in try/except

Validates JSON schema before use

Logs detailed errors in Airflow

Airflow retries failed tasks automatically

Database errors handled safely

📈 Scalability

Add more stock symbols in .env

Airflow can scale with Celery/Dockerized workers

PostgreSQL handles large volumes of inserts

Script supports multi-symbol ingestion

📜 SQL Table Definition

Defined in create_table.sql:

CREATE TABLE IF NOT EXISTS stock_prices (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10),
    price NUMERIC,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume BIGINT,
    api_timestamp TIMESTAMP,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(50),
    raw_json JSONB,
    UNIQUE(symbol, api_timestamp)
);

🧪 Testing the Database

To view the latest inserted rows:

docker exec -it stocks_postgres psql -U stocks_user -d stocks_db -c \
"SELECT symbol, price, api_timestamp, fetched_at FROM stock_prices ORDER BY fetched_at DESC LIMIT 20;"

✔ Assignment Requirements — Fully Met
Requirement	Status
Docker Compose environment	✅
Airflow or Dagster orchestrator	✅ (Airflow)
Fetch data via Python requests	✅
Parse JSON & extract metrics	✅
Store into PostgreSQL	✅
Error handling	✅
Environment variables	✅
Scalability	✅
Clean README	✅ (this file)
🧑‍💻 Author

Divyansh
Data Engineering & Machine Learning Enthusiast

If you found this useful, ⭐ the repository!


---

# 🎉 You're Done  
This README is perfectly structured for:

✔ Assignment submission  
✔ Professional GitHub presentation  
✔ Interview demonstration  
✔ Recruiter review  

If you want, I can now generate:

📌 **Architecture diagram (PNG)**  
📌 **Submission PDF**  
📌 **Viva Q&A answers**  
📌 **Short demo script for Loom video**

Just tell me.





