import streamlit as st


def initialize_session():

    defaults = {
        "authenticated": False,
        "employee_id": None,
        "first_name": None,
        "last_name": None,
        "role": None
    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


def login_user(user):

    st.session_state["authenticated"] = True
    st.session_state["employee_id"] = user["employee_id"]
    st.session_state["first_name"] = user["first_name"]
    st.session_state["last_name"] = user["last_name"]
    st.session_state["role"] = user["role"]


def logout_user():

    st.session_state.clear()