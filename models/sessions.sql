-- models/sessions.sql
-- Sessionization logic for product analytics
-- A new session starts after 30 minutes of inactivity

CREATE OR REPLACE TABLE sessions AS
WITH ordered_events AS (
    SELECT
        user_key,
        event_time,
        event_name,

        -- previous event timestamp per user
        LAG(event_time) OVER (
            PARTITION BY user_key
            ORDER BY event_time
        ) AS previous_event_time
    FROM events
),

session_flags AS (
    SELECT
        user_key,
        event_time,
        event_name,

        CASE
            WHEN previous_event_time IS NULL THEN 1
            WHEN event_time - previous_event_time > INTERVAL '30 minutes' THEN 1
            ELSE 0
        END AS is_new_session
    FROM ordered_events
),

session_ids AS (
    SELECT
        user_key,
        event_time,
        event_name,

        -- cumulative sum to generate session ids
        SUM(is_new_session) OVER (
            PARTITION BY user_key
            ORDER BY event_time
            ROWS UNBOUNDED PRECEDING
        ) AS session_number
    FROM session_flags
)

SELECT
    user_key,
    session_number,

    MIN(event_time) AS session_start,
    MAX(event_time) AS session_end,

    COUNT(*)        AS events_in_session,
    DATE_DIFF(
        'minute',
        MIN(event_time),
        MAX(event_time)
    ) AS session_duration_minutes
FROM session_ids
GROUP BY user_key, session_number;
