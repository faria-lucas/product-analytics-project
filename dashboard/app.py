import duckdb
import streamlit as st

con = duckdb.connect("analytics.duckdb", read_only=True)
tables = con.execute("SHOW TABLES").fetchall()



st.title("Product Analytics – Overview")

# --- Chart 1: DAU ---
st.subheader("Daily Active Users (DAU)")
dau = con.execute("""
    SELECT event_day, COUNT(DISTINCT user_key) AS dau
    FROM events
    GROUP BY event_day
    ORDER BY event_day
""").df()
st.line_chart(dau.set_index("event_day"))

# --- Chart 2: Activation Funnel ---
st.subheader("Activation Funnel")
funnel = con.execute("""
    SELECT
      COUNT(DISTINCT user_key) AS total_users,
      COUNT(DISTINCT CASE WHEN is_signed_up THEN user_key END) AS signed_up,
      COUNT(DISTINCT CASE WHEN is_activated THEN user_key END) AS activated
    FROM users
""").df()
st.dataframe(funnel)

# --- Chart 3: Session Duration ---
st.subheader("Session Duration (minutes)")
sessions = con.execute("""
    SELECT session_duration_minutes
    FROM sessions
""").df()
st.bar_chart(sessions)

# --- Tables ---
st.divider()

st.subheader("Events")
st.dataframe(con.execute("SELECT * FROM events").df())

st.subheader("Users")
st.dataframe(con.execute("SELECT * FROM users").df())

st.subheader("Sessions")
st.dataframe(con.execute("""
    SELECT user_key, session_start, session_end, session_duration_minutes
    FROM sessions
    ORDER BY session_start
""").df())
