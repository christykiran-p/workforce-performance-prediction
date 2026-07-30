from sqlalchemy import text

from src.database.mysql_connection import (
    get_engine
)


def get_manager_reportees(
    manager_id: int
):
    """
    Returns all active employees
    reporting to a manager.
    """

    engine = get_engine()

    query = text(
        """
        SELECT
            employee_id
        FROM employee_reporting
        WHERE reporting_manager_id = :manager_id
          AND reporting_status = 'Active'
        """
    )

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "manager_id": manager_id
            }
        )

        return [
            row.employee_id
            for row in result.fetchall()
        ]


def get_all_employee_ids():
    """
    Returns every employee
    in the organization.
    """

    engine = get_engine()

    query = text(
        """
        SELECT employee_id
        FROM employee
        """
    )

    with engine.connect() as conn:

        result = conn.execute(query)

        return [
            row.employee_id
            for row in result.fetchall()
        ]


def get_accessible_employee_ids(
    employee_id: int,
    role: str
):
    """
    Enterprise Security Layer

    Determines which employees
    the logged-in user can access.
    """

    if role in [
        "Admin",
        "Leadership",
        "HR"
    ]:

        return get_all_employee_ids()

    if role == "Manager":

        return get_manager_reportees(
            employee_id
        )

    return []