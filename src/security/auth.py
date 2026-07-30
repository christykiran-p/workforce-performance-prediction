from sqlalchemy import text

from src.database.mysql_connection import (
    get_engine
)

from src.security.role_manager import (
    get_employee_role
)


def authenticate_user(
    employee_id,
    first_name,
    last_name,
    selected_role,
    password
):

    # =====================================
    # Password Validation
    # =====================================

    if selected_role == "Admin":

        if password != "admin4321":
            return None

    else:

        if password != "admin1234":
            return None

    engine = get_engine()

    query = text(
        """
        SELECT
            employee_id,
            first_name,
            last_name
        FROM employee
        WHERE employee_id = :employee_id
        """
    )

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "employee_id": employee_id
            }
        )

        employee = result.fetchone()

    if not employee:

        return None

    if (
        employee.first_name.strip().lower()
        !=
        first_name.strip().lower()
    ):
        return None

    if (
        employee.last_name.strip().lower()
        !=
        last_name.strip().lower()
    ):
        return None

    actual_role = get_employee_role(
        employee_id
    )

    if actual_role != selected_role:

        return None

    return {
        "employee_id": employee.employee_id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "role": actual_role
    }