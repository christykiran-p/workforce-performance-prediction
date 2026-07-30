from pathlib import Path

from src.database.mysql_connection import load_table


RAW_DATA_PATH = Path("data/raw")


TABLES = [
    "employee",
    "employee_performance",
    "employee_attendance",
    "employee_reporting",
    "leave_balance",
    "org_structure",
]


def extract_mysql_tables_to_parquet():
    RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)

    for table in TABLES:
        df = load_table(table)
        output_path = RAW_DATA_PATH / f"{table}.parquet"
        df.to_parquet(output_path, index=False)
        print(f"Extracted {table}: {len(df)} rows -> {output_path}")


if __name__ == "__main__":
    extract_mysql_tables_to_parquet()