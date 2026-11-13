import streamlit as st
import re
from utils.auth import login_user
from utils.cookies import set_cookie
from utils.auth import save_session

st.set_page_config(layout="centered")


def is_valid_email(email):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", email)


st.title("🔐 Sign In")

with st.form("sign_in_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    sign_in_btn = st.form_submit_button("Sign In")

    if sign_in_btn:
        success, result = login_user(email, password)

        if success:
            st.session_state.user = result
            st.session_state.profile = result.get("profile", {})
            st.session_state.career = result.get("career", {})

            # cookie (fast restore)
            set_cookie("user_email", result["email"])

             # file (restart restore)
            save_session(result["email"])

            st.success("Logged in successfully")
            st.switch_page("streamlit_app.py")

        else:
            st.error(result)