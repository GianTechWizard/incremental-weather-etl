from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

PROJECT_PATH = "/home/gian/airflow/dags/incremental_weather_etl"
sys.path.append(PROJECT_PATH)

from main import run_etl

default_args = {
    "owner": "gian",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="weather_incremental_etl",
    default_args=default_args,
    description="Incremental Weather ETL Pipeline",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "weather", "incremental"],
) as dag:

    run_pipeline = PythonOperator(
        task_id="run_incremental_weather_etl",
        python_callable=run_etl,
        op_kwargs={"city": "Jakarta"},
    )

    run_pipeline
