import streamlit as st
import re
from utils.auth import create_user

st.set_page_config(layout="centered")

def is_valid_email(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)

def is_strong_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain number"
    return True, "✅ Strong password"

st.title("📝 Create Account")

with st.form("signup_form"):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
    with col2:
        last_name = st.text_input("Last Name")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")

    create_account = st.form_submit_button("Create Account")

    if create_account:
        if not first_name or not last_name:
            st.error("Name fields required")
        elif not is_valid_email(email):
            st.error("Invalid email format")
        elif password != confirm:
            st.error("Passwords do not match")
        else:
            is_strong, msg = is_strong_password(password)
            if not is_strong:
                st.error(msg)
            else:
                success, result = create_user(email, password, first_name, last_name)
                if success:
                    st.success("Account created. Please sign in.")
                else:
                    st.error(result)