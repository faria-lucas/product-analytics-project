-- models/users.sql
-- User-level analytics model

CREATE OR REPLACE TABLE users AS
WITH base_events AS (
    SELECT
        user_key,
        event_name,
        event_time
    FROM events
),

aggregated AS (
    SELECT
        user_key,

        -- first time we ever saw this user
        MIN(event_time) AS first_seen_at,

        -- signup moment
        MIN(CASE
            WHEN event_name = 'signup' THEN event_time
        END) AS signup_at,

        -- activation moment (simple definition for v1)
        MIN(CASE
            WHEN event_name = 'onboarding_completed' THEN event_time
        END) AS activation_at,

        -- last activity
        MAX(event_time) AS last_activity_at

    FROM base_events
    GROUP BY user_key
)

SELECT
    user_key,
    first_seen_at,
    signup_at,
    activation_at,
    last_activity_at,

    -- useful flags
    signup_at IS NOT NULL      AS is_signed_up,
    activation_at IS NOT NULL  AS is_activated
FROM aggregated;
