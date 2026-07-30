from sqlalchemy import text

from src.database.mysql_connection import (
    get_engine
)


def get_employee_role(
    employee_id
):

    engine = get_engine()

    # =====================================
    # Admin
    # =====================================

    if employee_id == 1:

        return "Admin"

    # =====================================
    # Leadership
    # =====================================

    if employee_id in [
        2,
        3,
        4,
        5,
        6,
        7
    ]:

        return "Leadership"

    # =====================================
    # HR
    # =====================================

    hr_query = text(
        """
        SELECT department
        FROM employee
        WHERE employee_id = :employee_id
        """
    )

    with engine.connect() as conn:

        result = conn.execute(
            hr_query,
            {
                "employee_id": employee_id
            }
        )

        row = result.fetchone()

    if row:

        if (
            str(row.department)
            .strip()
            .lower()
            ==
            "human resources"
        ):

            return "HR"

    # =====================================
    # Manager
    # =====================================

    manager_query = text(
        """
        SELECT COUNT(*)
        AS team_size
        FROM employee_reporting
        WHERE reporting_manager_id =
              :employee_id
        """
    )

    with engine.connect() as conn:

        result = conn.execute(
            manager_query,
            {
                "employee_id": employee_id
            }
        )

        team_size = result.scalar()

    if team_size > 0:

        return "Manager"

    return None