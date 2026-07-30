import streamlit as st

from src.security.session_manager import (
    initialize_session
)


def require_login():

    initialize_session()

    if not st.session_state.authenticated:

        st.error("Please login first.")

        st.info(
            "Open the Login page and authenticate to continue."
        )

        st.stop()


def require_role(
    allowed_roles: list
):

    require_login()

    if st.session_state.role not in allowed_roles:

        st.error(
            "You are not authorized to access this page."
        )

        st.stop()