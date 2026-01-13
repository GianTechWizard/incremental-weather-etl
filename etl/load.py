import pandas as pd
from sqlalchemy import create_engine
from config.db_config import DB_CONFIG
from etl.metadata import (
    get_last_processed_timestamp,
    update_last_processed_timestamp,
)
from etl.logger import setup_logger


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )


def load_weather_data(df):
    logger = setup_logger()
    logger.info("Starting load process")

    engine = get_engine()
    last_ts = get_last_processed_timestamp()

    df["extracted_at"] = pd.to_datetime(df["extracted_at"])

    df_new = df[df["extracted_at"] > last_ts]

    if df_new.empty:
        logger.info("No new data to load")
        return

    df_new.to_sql(
        "weather_fact",
        engine,
        if_exists="append",
        index=False,
        method="multi"
    )

    latest_ts = df_new["extracted_at"].max()
    update_last_processed_timestamp(latest_ts)

    logger.info(f"{len(df_new)} new records loaded successfully")


if __name__ == "__main__":
    from etl.extract import extract_weather_data
    from etl.transform import transform_weather_data
    from etl.validate import validate_weather_data

    raw = extract_weather_data(city="Jakarta")
    record = transform_weather_data(raw)

    if validate_weather_data(record):
        df = pd.DataFrame([record])
        load_weather_data(df)
    else:
        print("Data validation failed.")
