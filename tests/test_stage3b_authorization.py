from unittest.mock import patch

from src.security.authorization import (
    require_login,
    require_role
)


# =====================================================
# Authentication Required
# =====================================================

@patch("src.security.authorization.initialize_session")
@patch("streamlit.stop")
@patch("streamlit.error")
@patch("streamlit.session_state")
def test_require_login_not_authenticated(
    mock_session,
    mock_error,
    mock_stop,
    mock_initialize
):

    mock_session.authenticated = False

    require_login()

    mock_error.assert_called_once()

    mock_stop.assert_called_once()


@patch("src.security.authorization.initialize_session")
@patch("streamlit.session_state")
def test_require_login_authenticated(
    mock_session,
    mock_initialize
):

    mock_session.authenticated = True

    require_login()


# =====================================================
# Role Authorization
# =====================================================

@patch("src.security.authorization.require_login")
@patch("streamlit.session_state")
def test_require_role_authorized(
    mock_session,
    mock_require_login
):

    mock_session.role = "Admin"

    require_role(
        [
            "Admin"
        ]
    )


@patch("src.security.authorization.require_login")
@patch("streamlit.stop")
@patch("streamlit.error")
@patch("streamlit.session_state")
def test_require_role_unauthorized(
    mock_session,
    mock_error,
    mock_stop,
    mock_require_login
):

    mock_session.role = "Manager"

    require_role(
        [
            "Admin"
        ]
    )

    mock_error.assert_called_once()

    mock_stop.assert_called_once()