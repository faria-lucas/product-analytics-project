import duckdb
import streamlit as st

con = duckdb.connect("analytics.duckdb", read_only=True)
tables = con.execute("SHOW TABLES").fetchall()
print(tables)

# Exemplo: selecionar tudo da tabela
df = con.execute("SELECT * FROM events").fetchdf()
print(df.head())

df = con.execute("SELECT * FROM sessions").fetchdf()
print(df.head())

df = con.execute("SELECT * FROM users").fetchdf()
print(df.head())


st.title("Product Analytics – Overview")

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
