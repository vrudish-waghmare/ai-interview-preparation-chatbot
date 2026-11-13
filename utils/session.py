import streamlit as st
from utils.cookies import get_cookie
from utils.auth import load_users, load_session


def restore_session():
    """
    Restore user session from cookie or session file
    Respects logout flag to prevent re-authentication
    """
    # Don't restore if explicitly logged out
    if st.session_state.get("is_logged_out", False):
        return
    
    if "user" not in st.session_state:
        # Check cookie first
        user_email = get_cookie("user_email")

        # Fallback if cookie fails
        if not user_email:
            user_email = load_session()

        if user_email:
            users = load_users()
            for u in users:
                if u["email"] == user_email:
                    st.session_state.user = u
                    st.session_state.profile = u.get("profile", {})
                    st.session_state.career = u.get("career", {})


def require_login():
    """
    Require user to be logged in
    Blocks access if not authenticated
    """
    restore_session()

    if "user" not in st.session_state:
        st.warning("🔐 Please login first")
        st.stop()