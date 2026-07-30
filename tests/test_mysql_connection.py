from src.database.mysql_connection import get_engine, load_table


def test_get_engine():
    engine = get_engine()
    assert engine is not None


def test_load_employee_table():
    df = load_table("employee")
    assert df is not None
    assert len(df) > 0