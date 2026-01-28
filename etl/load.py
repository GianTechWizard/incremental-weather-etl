import pandas as pd
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.dialects.postgresql import insert
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

    # =========================
    # GET LAST PROCESSED TS
    # =========================
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT last_processed_ts
                FROM etl_metadata
                WHERE pipeline_name = :pipeline_name
            """),
            {"pipeline_name": "weather_pipeline"}
        ).fetchone()

        last_ts = result[0] if result else None

    # =========================
    # NORMALIZE TIMESTAMP
    # =========================
    df["weather_timestamp"] = pd.to_datetime(df["weather_timestamp"], utc=True)

    if last_ts is not None:
        last_ts = pd.to_datetime(last_ts, utc=True)
        df_new = df[df["weather_timestamp"] > last_ts]
    else:
        df_new = df

    if df_new.empty:
        logger.info("No new data to load")
        return

    # =========================
    # LOAD DATA (SQLALCHEMY CORE + ON CONFLICT)
    # =========================
    metadata = MetaData()
    weather_fact = Table(
        "weather_fact",
        metadata,
        autoload_with=engine,
        schema="public"
    )

    # =========================
    # ALIGN COLUMNS EXPLICITLY
    # =========================
    expected_columns = [
        "city",
        "country",
        "temperature",
        "humidity",
        "weather_description",
        "wind_speed",
        "weather_timestamp",
        "extracted_at",
    ]

    df_new = df_new[expected_columns]

    df_new["weather_timestamp"] = pd.to_datetime(df_new["weather_timestamp"]).dt.tz_localize(None)
    df_new["extracted_at"] = pd.to_datetime(df_new["extracted_at"]).dt.tz_localize(None)

    records = df_new.to_dict(orient="records")

    stmt = insert(weather_fact).values(records)
    stmt = stmt.on_conflict_do_nothing(
        index_elements=["city", "extracted_at"]
    )

    # =========================
    # EXECUTE INSERT (GUARD FOR DUPLICATES)
    # =========================
    with engine.begin() as conn:
        result = conn.execute(stmt)

        if result.rowcount == 0:
            logger.info("No new rows inserted (duplicate data)")
            return

    # =========================
    # UPDATE METADATA
    # =========================
    latest_ts = df_new["weather_timestamp"].max()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO etl_metadata (pipeline_name, last_processed_ts)
                VALUES (:pipeline_name, :ts)
                ON CONFLICT (pipeline_name)
                DO UPDATE SET last_processed_ts = EXCLUDED.last_processed_ts
            """),
            {
                "pipeline_name": "weather_pipeline",
                "ts": latest_ts
            }
        )

    logger.info(f"{len(df_new)} new records loaded successfully")


if __name__ == "__main__":
    from etl.extract import extract_weather_data
    from etl.transform import transform_weather_data
    from etl.validate import validate_weather_data

    raw = extract_weather_data(city="Jakarta")
    record = transform_weather_data(raw)

    is_valid, _ = validate_weather_data(record)

    if is_valid:
        df = pd.DataFrame([record])
        load_weather_data(df)
    else:
        print("Data validation failed.")
