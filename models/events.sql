-- models/events.sql
-- Canonical events table for product analytics

CREATE OR REPLACE TABLE events AS
SELECT
    event_id,
    event_name,

    -- Timestamp UTC (preserves hour-level analysis)
    event_time,

    -- Date helper for partitions and daily aggregations
    event_date,

    user_key,
    user_id,
    anonymous_id,

    -- Lightweight analytical helpers
    DATE(event_time)               AS event_day,
    EXTRACT(hour FROM event_time)  AS event_hour,

    -- Semi-structured properties (kept flexible on purpose)
    properties
FROM read_parquet('data/parquet/events.parquet');
