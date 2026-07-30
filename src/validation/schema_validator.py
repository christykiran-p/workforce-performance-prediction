from src.database.mysql_connection import get_engine

REQUIRED_TABLES = [
    "employee",
    "employee_performance",
    "employee_attendance",
    "employee_reporting",
    "leave_balance",
    "org_structure",
]


def validate_required_tables():
    engine = get_engine()

    query = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = DATABASE();
    """

    with engine.connect() as connection:
        result = connection.exec_driver_sql(query)
        existing_tables = [row[0].lower() for row in result.fetchall()]

    missing_tables = [
        table for table in REQUIRED_TABLES
        if table.lower() not in existing_tables
    ]

    return {
        "existing_tables": existing_tables,
        "missing_tables": missing_tables,
        "is_valid": len(missing_tables) == 0,
    }