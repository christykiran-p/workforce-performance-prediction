import streamlit as st

from src.security.session_manager import (
    initialize_session,
    login_user,
    logout_user,
)

from src.security.auth import (
    authenticate_user,
)

from src.database.mysql_connection import (
    load_table,
)

from src.validation.schema_validator import (
    validate_required_tables,
)

# ==========================================================
# Initialize Session
# ==========================================================

initialize_session()

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Workforce Performance Intelligence Platform",
    page_icon="📊",
    layout="wide",
)

# ==========================================================
# LOGIN SCREEN
# ==========================================================

if not st.session_state.authenticated:

    st.title("Workforce Performance Intelligence Platform")

    st.caption(
        "Predict. Understand. Explain. Calibrate. Recommend. Decide. Act. Learn."
    )

    st.divider()

    st.subheader("User Login")

    employee_id = st.number_input(
        "Employee ID",
        min_value=1,
        step=1,
    )

    first_name = st.text_input(
        "First Name"
    )

    last_name = st.text_input(
        "Last Name"
    )

    role = st.selectbox(
        "Role",
        [
            "Admin",
            "Leadership",
            "HR",
            "Manager",
        ],
    )

    password = st.text_input(
        "Password",
        type="password",
    )

    if st.button(
        "Login",
        use_container_width=True,
    ):

        user = authenticate_user(
            employee_id,
            first_name,
            last_name,
            role,
            password,
        )

        if user:

            login_user(user)

            st.success(
                f"Welcome {user['first_name']}!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid credentials."
            )

    st.stop()

# ==========================================================
# HOME DASHBOARD
# ==========================================================

st.title(
    "Workforce Performance Intelligence Platform"
)

st.caption(
    "Predict. Understand. Explain. Calibrate. Recommend. Decide. Act. Learn."
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Welcome")

st.sidebar.success(
    f"""
{st.session_state.first_name}
{st.session_state.last_name}

Role : {st.session_state.role}
"""
)

st.sidebar.divider()

if st.sidebar.button(
    "Validate Database Schema",
    use_container_width=True,
):

    result = validate_required_tables()

    if result["is_valid"]:

        st.sidebar.success(
            "Database schema validation passed."
        )

    else:

        st.sidebar.error(
            "Missing tables found."
        )

        st.sidebar.write(
            result["missing_tables"]
        )

st.sidebar.divider()

if st.sidebar.button(
    "Logout",
    use_container_width=True,
):

    logout_user()

    st.rerun()

role = st.session_state.role

st.divider()

# ==========================================================
# ADMIN
# ==========================================================

if role == "Admin":

    st.header("Administrator Dashboard")

    employee_df = load_table("employee")
    performance_df = load_table("employee_performance")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Employees",
        len(employee_df),
    )

    c2.metric(
        "Performance Records",
        len(performance_df),
    )

    c3.metric(
        "Departments",
        employee_df["department"].nunique(),
    )

    st.info(
        """
Administrator Privileges

• Platform Administration

• User Management

• RBAC Management

• Developers Quality Dashboard

• Database Validation
"""
    )

    st.subheader(
        "Employee Preview"
    )

    st.dataframe(
        employee_df.head(),
        use_container_width=True,
    )

# ==========================================================
# LEADERSHIP
# ==========================================================

elif role == "Leadership":

    st.header("Leadership Dashboard")

    employee_df = load_table("employee")
    performance_df = load_table("employee_performance")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Employees",
        len(employee_df),
    )

    c2.metric(
        "Performance Records",
        len(performance_df),
    )

    c3.metric(
        "Departments",
        employee_df["department"].nunique(),
    )

    st.subheader(
        "Employee Preview"
    )

    st.dataframe(
        employee_df.head(),
        use_container_width=True,
    )

# ==========================================================
# HR
# ==========================================================

elif role == "HR":

    st.header("HR Dashboard")

    employee_df = load_table("employee")
    leave_df = load_table("leave_balance")

    c1, c2 = st.columns(2)

    c1.metric(
        "Employees",
        len(employee_df),
    )

    c2.metric(
        "Leave Records",
        len(leave_df),
    )

    st.subheader(
        "Leave Balance"
    )

    st.dataframe(
        leave_df.head(),
        use_container_width=True,
    )

# ==========================================================
# MANAGER
# ==========================================================

elif role == "Manager":

    st.header("Manager Dashboard")

    reporting_df = load_table(
        "employee_reporting"
    )

    performance_df = load_table(
        "employee_performance"
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Reporting Records",
        len(reporting_df),
    )

    c2.metric(
        "Performance Records",
        len(performance_df),
    )

    st.subheader(
        "Reporting Hierarchy"
    )

    st.dataframe(
        reporting_df.head(),
        use_container_width=True,
    )