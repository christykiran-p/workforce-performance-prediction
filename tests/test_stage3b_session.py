from unittest.mock import patch
import streamlit as st

from src.security.session_manager import (
    initialize_session,
    login_user,
    logout_user
)


# =====================================================
# Initialize Session
# =====================================================

@patch.object(st, "session_state", {})
def test_initialize_session():

    initialize_session()

    assert st.session_state["authenticated"] is False
    assert st.session_state["employee_id"] is None
    assert st.session_state["first_name"] is None
    assert st.session_state["last_name"] is None
    assert st.session_state["role"] is None


# =====================================================
# Login User
# =====================================================

@patch.object(st, "session_state", {})
def test_login_user():

    user = {
        "employee_id": 1,
        "first_name": "Christy",
        "last_name": "Kiran",
        "role": "Admin"
    }

    login_user(user)

    assert st.session_state["authenticated"] is True
    assert st.session_state["employee_id"] == 1
    assert st.session_state["first_name"] == "Christy"
    assert st.session_state["last_name"] == "Kiran"
    assert st.session_state["role"] == "Admin"


# =====================================================
# Logout User
# =====================================================

@patch.object(st, "session_state", {
    "authenticated": True,
    "employee_id": 1,
    "first_name": "Christy",
    "last_name": "Kiran",
    "role": "Admin"
})
def test_logout_user():

    logout_user()

    assert len(st.session_state) == 0