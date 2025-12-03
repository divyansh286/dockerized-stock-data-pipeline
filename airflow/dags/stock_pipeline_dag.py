import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="stock_data_pipeline",
    default_args=default_args,
    description="Fetch stock data and update PostgreSQL",
    schedule_interval="@hourly",
    start_date=days_ago(1),
    catchup=False,
    tags=["stocks"],
):

    run_fetch_script = BashOperator(
        task_id="run_fetch_script",
        bash_command="python /opt/airflow/scripts/fetch_and_update.py",
        env={
            "ALPHA_VANTAGE_API_KEY": os.getenv("ALPHA_VANTAGE_API_KEY"),
            "STOCK_SYMBOL": os.getenv("STOCK_SYMBOL", "AAPL"),
            "POSTGRES_HOST": os.getenv("POSTGRES_HOST", "postgres"),
            "POSTGRES_PORT": os.getenv("POSTGRES_PORT", "5432"),
            "POSTGRES_DB": os.getenv("POSTGRES_DB", "stocks_db"),
            "POSTGRES_USER": os.getenv("POSTGRES_USER", "stocks_user"),
            "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD", "stocks_pass"),
        }
    )
