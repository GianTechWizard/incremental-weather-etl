from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# =========================
# PATH PROJECT ETL
# =========================
PROJECT_PATH = "/home/gian/airflow/dags/incremental_weather_etl"
sys.path.append(PROJECT_PATH)

from main import extract_task, transform_task, load_task


# =========================
# DEFAULT ARGS
# =========================
default_args = {
    "owner": "gian",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "sla": timedelta(minutes=10),
}


# =========================
# DAG DEFINITION
# =========================
with DAG(
    dag_id="weather_incremental_etl",
    default_args=default_args,
    description="Incremental Weather ETL Pipeline",
    schedule_interval="@hourly",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "weather", "incremental"],
) as dag:

    dag.doc_md = """
    ### 🌦️ Incremental Weather ETL Pipeline

    **Flow:**
    1. Extract weather data from OpenWeather API
    2. Transform + validate data
    3. Load data incrementally into PostgreSQL

    **Features:**
    - Incremental load
    - Retry & SLA
    - Modular ETL
    - Airflow best practice (task-based)
    """

    # =========================
    # TASK: EXTRACT
    # =========================
    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=extract_task,
        op_kwargs={"city": "Jakarta"},
    )

    # =========================
    # TASK: TRANSFORM + VALIDATE
    # =========================
    transform = PythonOperator(
        task_id="transform_weather",
        python_callable=transform_task,
    )

    # =========================
    # TASK: LOAD
    # =========================
    load = PythonOperator(
        task_id="load_weather",
        python_callable=load_task,
    )

    # =========================
    # TASK DEPENDENCY
    # =========================
    extract >> transform >> load
