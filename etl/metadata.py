from sqlalchemy import create_engine, text
from datetime import datetime, timezone
from config.db_config import DB_CONFIG

PIPELINE_NAME = "weather_pipeline"


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )


def get_last_processed_timestamp():
    engine = get_engine()

    query = text("""
        SELECT last_processed_ts
        FROM etl_metadata
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"pipeline_name": PIPELINE_NAME}).fetchone()

    if result is None or result[0] is None:
        return datetime.min.replace(tzinfo=timezone.utc)

    return result[0]


def update_last_processed_timestamp(new_ts):
    engine = get_engine()

    query = text("""
        UPDATE etl_metadata
        SET last_processed_ts = :last_ts
        WHERE pipeline_name = :pipeline_name
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "pipeline_name": PIPELINE_NAME,
                "last_ts": new_ts,
            },
        )
