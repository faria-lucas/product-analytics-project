import duckdb
from pathlib import Path


DB_PATH = "analytics.duckdb"
SQL_MODELS = [
    "models/events.sql",
    "models/sessions.sql",
    "models/users.sql",
]


def run():
    con = duckdb.connect(DB_PATH)

    for sql_file in SQL_MODELS:
        print(f"Running {sql_file}")
        con.execute(Path(sql_file).read_text())

    con.close()
    print("Pipeline completed successfully")


if __name__ == "__main__":
    run()
