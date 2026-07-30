from src.security.auth import (
    authenticate_user
)

from src.security.role_manager import (
    get_employee_role
)

from src.security.data_access import (
    get_manager_reportees,
    get_all_employee_ids,
    get_accessible_employee_ids
)


# =====================================================
# Authentication
# =====================================================

def test_admin_login():

    user = authenticate_user(
        1,
        "Christy",
        "Kiran",
        "Admin",
        "admin4321"
    )

    assert user is not None
    assert user["role"] == "Admin"


def test_manager_invalid_password():

    user = authenticate_user(
        212,
        "Karthik",
        "Sharma",
        "Manager",
        "wrongpassword"
    )

    assert user is None


# =====================================================
# Role Mapping
# =====================================================

def test_admin_role():

    assert get_employee_role(1) == "Admin"


def test_leadership_role():

    assert get_employee_role(2) == "Leadership"


def test_manager_role():

    assert get_employee_role(212) == "Manager"


# =====================================================
# Data Access Layer
# =====================================================

def test_all_employee_ids():

    employees = get_all_employee_ids()

    assert isinstance(
        employees,
        list
    )

    assert len(employees) > 0


def test_manager_reportees():

    reportees = get_manager_reportees(212)

    assert isinstance(
        reportees,
        list
    )

    assert len(reportees) > 0


def test_admin_access():

    employees = get_accessible_employee_ids(
        1,
        "Admin"
    )

    assert len(employees) == len(
        get_all_employee_ids()
    )


def test_leadership_access():

    employees = get_accessible_employee_ids(
        2,
        "Leadership"
    )

    assert len(employees) == len(
        get_all_employee_ids()
    )


def test_hr_access():

    employees = get_accessible_employee_ids(
        8,
        "HR"
    )

    assert len(employees) == len(
        get_all_employee_ids()
    )


def test_manager_access():

    employees = get_accessible_employee_ids(
        212,
        "Manager"
    )

    reportees = get_manager_reportees(212)

    assert len(employees) == len(reportees)


def test_unknown_role():

    employees = get_accessible_employee_ids(
        212,
        "Intern"
    )

    assert employees == []

# =====================================================
# Authentication - Negative Test Cases
# =====================================================

def test_invalid_employee():

    user = authenticate_user(
        9999,
        "Test",
        "User",
        "Admin",
        "admin4321"
    )

    assert user is None


def test_invalid_first_name():

    user = authenticate_user(
        1,
        "WrongName",
        "Kiran",
        "Admin",
        "admin4321"
    )

    assert user is None


def test_invalid_last_name():

    user = authenticate_user(
        1,
        "Christy",
        "WrongLastName",
        "Admin",
        "admin4321"
    )

    assert user is None


def test_invalid_role():

    user = authenticate_user(
        1,
        "Christy",
        "Kiran",
        "Manager",
        "admin1234"
    )

    assert user is None

    