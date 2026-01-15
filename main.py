import pandas as pd

from etl.extract import extract_weather_data
from etl.transform import transform_weather_data
from etl.validate import validate_weather_data, data_quality_report
from etl.load import load_weather_data
from etl.logger import setup_logger


# =========================
# AIRFLOW TASK: EXTRACT
# =========================
def extract_task(city: str = "Jakarta"):
    logger = setup_logger()
    logger.info("=== START WEATHER INCREMENTAL ETL PIPELINE ===")

    logger.info("Step 1: Extracting data from OpenWeather API")
    raw_data = extract_weather_data(city=city)

    return raw_data


# =========================
# AIRFLOW TASK: TRANSFORM + VALIDATE
# =========================
def transform_task(raw_data):
    logger = setup_logger()

    logger.info("Step 2: Transforming raw data")
    record = transform_weather_data(raw_data)

    logger.info("Step 3: Generating data quality report")
    report = data_quality_report(record)
    logger.info(f"Data Quality Report: {report}")

    logger.info("Step 4: Validating transformed data")
    is_valid, errors = validate_weather_data(record)

    if not is_valid:
        logger.error(f"Data validation failed: {errors}")
        raise ValueError(f"Validation failed: {errors}")

    return record


# =========================
# AIRFLOW TASK: LOAD
# =========================
def load_task(record):
    logger = setup_logger()

    logger.info("Step 5: Loading data incrementally to PostgreSQL")
    df = pd.DataFrame([record])
    load_weather_data(df)

    logger.info("=== ETL PIPELINE FINISHED SUCCESSFULLY ===")
    return True


# =========================
# STANDALONE ETL (NON-AIRFLOW)
# =========================
def run_etl(city: str = "Jakarta"):
    logger = setup_logger()
    logger.info("=== START WEATHER INCREMENTAL ETL PIPELINE ===")

    logger.info("Step 1: Extracting data from OpenWeather API")
    raw_data = extract_weather_data(city=city)

    logger.info("Step 2: Transforming raw data")
    record = transform_weather_data(raw_data)

    logger.info("Step 3: Generating data quality report")
    report = data_quality_report(record)
    logger.info(f"Data Quality Report: {report}")

    logger.info("Step 4: Validating transformed data")
    is_valid, errors = validate_weather_data(record)

    if not is_valid:
        logger.error(f"Data validation failed: {errors}")
        raise ValueError(f"Validation failed: {errors}")

    logger.info("Step 5: Loading data incrementally to PostgreSQL")
    df = pd.DataFrame([record])
    load_weather_data(df)

    logger.info("=== ETL PIPELINE FINISHED SUCCESSFULLY ===")
    return True


if __name__ == "__main__":
    run_etl()
