-- Weather fact table
CREATE TABLE IF NOT EXISTS weather_fact (
    city TEXT,
    country TEXT,
    temperature DOUBLE PRECISION,
    humidity INTEGER,
    weather_description TEXT,
    wind_speed DOUBLE PRECISION,
    weather_timestamp TIMESTAMP,
    extracted_at TIMESTAMP,
    PRIMARY KEY (city, extracted_at)
);

-- ETL metadata table
CREATE TABLE IF NOT EXISTS etl_metadata (
    pipeline_name TEXT PRIMARY KEY,
    last_processed_ts TIMESTAMP
);

-- Initial metadata record
INSERT INTO etl_metadata (pipeline_name, last_processed_ts)
VALUES ('weather_pipeline', '1970-01-01 00:00:00')
ON CONFLICT (pipeline_name) DO NOTHING;