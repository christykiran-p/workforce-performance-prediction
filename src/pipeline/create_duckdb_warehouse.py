from pathlib import Path

import duckdb


PROCESSED_PATH = Path("data/processed")
WAREHOUSE_PATH = Path("data/warehouse")
DUCKDB_FILE = WAREHOUSE_PATH / "workforce_analytics.duckdb"


def create_duckdb_warehouse() -> None:
    WAREHOUSE_PATH.mkdir(parents=True, exist_ok=True)

    processed_file = PROCESSED_PATH / "employee_analytics_dataset.parquet"

    conn = duckdb.connect(str(DUCKDB_FILE))

    conn.execute("""
        CREATE OR REPLACE TABLE employee_analytics AS
        SELECT *
        FROM read_parquet('data/processed/employee_analytics_dataset.parquet')
    """)

    row_count = conn.execute(
        "SELECT COUNT(*) FROM employee_analytics"
    ).fetchone()[0]

    column_count = conn.execute(
        "SELECT COUNT(*) FROM information_schema.columns WHERE table_name = 'employee_analytics'"
    ).fetchone()[0]

    print(f"DuckDB warehouse created -> {DUCKDB_FILE}")
    print(f"Table created: employee_analytics")
    print(f"Total rows: {row_count}")
    print(f"Total columns: {column_count}")

    conn.close()


if __name__ == "__main__":
    create_duckdb_warehouse()