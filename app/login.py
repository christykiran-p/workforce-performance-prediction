import streamlit as st

from src.security.auth import (
    authenticate_user
)

from src.security.session_manager import (
    initialize_session,
    login_user,
    logout_user
)


initialize_session()

st.set_page_config(
    page_title="Login",
    layout="centered"
)

st.title(
    "Workforce Performance Prediction"
)

st.subheader(
    "User Login"
)

employee_id = st.number_input(
    "Employee ID",
    min_value=1,
    step=1
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
        "Manager"
    ]
)

password = st.text_input(
    "Password",
    type="password"
)

if st.button(
    "Login"
):

    user = authenticate_user(
        employee_id,
        first_name,
        last_name,
        role,
        password
    )

    if user:

        login_user(user)

        st.switch_page(
            "main.py"
        )
    else:

        st.error(
            "Invalid credentials."
        )

if st.session_state.authenticated:

    st.success(
        f"""
Welcome

{st.session_state.first_name}
{st.session_state.last_name}

Role:
{st.session_state.role}
"""
    )

    col1, col2 = st.columns(
        [4, 1]
    )

    with col2:

        if st.button(
            "Logout"
        ):

            logout_user()

            st.rerun()