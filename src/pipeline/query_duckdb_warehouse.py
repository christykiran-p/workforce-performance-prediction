import duckdb
from pathlib import Path

DUCKDB_FILE = Path("data/warehouse/workforce_analytics.duckdb")


def run_analytics_queries() -> None:
    conn = duckdb.connect(str(DUCKDB_FILE))

    print("\nTotal Employees")
    print(conn.execute("""
        SELECT COUNT(*) AS total_employees
        FROM employee_analytics
    """).df())

    print("\nAverage Performance by Department")
    print(conn.execute("""
        SELECT
            department,
            ROUND(AVG(avg_performance_score), 2) AS avg_performance_score,
            COUNT(*) AS employee_count
        FROM employee_analytics
        GROUP BY department
        ORDER BY avg_performance_score DESC
    """).df())

    print("\nTop 10 Employees by Performance")
    print(conn.execute("""
        SELECT
            employee_id,
            first_name,
            last_name,
            department,
            avg_performance_score,
            attendance_rate,
            total_leave_used
        FROM employee_analytics
        ORDER BY avg_performance_score DESC
        LIMIT 10
    """).df())

    print("\nDepartment Attendance Summary")
    print(conn.execute("""
        SELECT
            department,
            ROUND(AVG(attendance_rate), 2) AS avg_attendance_rate,
            ROUND(AVG(total_overtime_hours), 2) AS avg_overtime_hours,
            ROUND(AVG(total_shortfall_hours), 2) AS avg_shortfall_hours
        FROM employee_analytics
        GROUP BY department
        ORDER BY avg_attendance_rate DESC
    """).df())

    conn.close()


if __name__ == "__main__":
    run_analytics_queries()