import streamlit as st
import re
from streamlit_option_menu import option_menu
from utils.auth import is_logged_in, logout_user
from utils.auth import load_users, save_users
from utils.session import require_login
from utils.logout_btn import logout_button, logout_confirmation_modal

st.set_page_config(layout="wide")


# auto login from cookie
require_login()


# auto sign in
if not is_logged_in():
    st.warning("Please sign in first")
    if st.button("Go to Sign In"):
        st.switch_page("pages/sign_in.py")
    st.stop()

user = st.session_state.get("user", {})


# header
col1, col2, col3 = st.columns([6, 2, 1])

with col1:
    st.title("👤 Profile Settings")

with col2:
    st.write(f"**{user.get('email')}**")

with col3:
    logout_button()


logout_confirmation_modal()


st.write("Manage your account information and preferences")


# menu
selected = option_menu(
    None,
    ['Profile', 'Career', 'Notifications', 'Privacy', 'Achievements'],
    orientation='horizontal'
)


# profile tab
if selected == 'Profile':
    st.subheader("Personal Information")
    
    profile = st.session_state.get("profile", {})

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", value=profile.get("first_name", ""))
    with col2:
        last_name = st.text_input("Last Name", value=profile.get("last_name", ""))

    email_address = st.text_input("Email", value=user.get("email", ""), disabled=True)
    st.caption("Email cannot be changed. Contact support if you need to update it.")

    col1, col2 = st.columns(2)
    with col1:
        phone_number = st.text_input("Phone", value=profile.get("phone", ""))
    with col2:
        location = st.text_input("Location", value=profile.get("location", ""))

    bio = st.text_area("Bio", value=profile.get("bio", ""))

    if st.button(":material/save: Save Changes", key='profile-save-btn'):
        # Save to session
        st.session_state.profile = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email_address,
            "phone": phone_number,
            "location": location,
            "bio": bio
        }

        # Load all users
        users = load_users()

        # Update current user
        for u in users:
            if u["email"] == st.session_state.user["email"]:
                u["profile"] = st.session_state.profile

        # Save back to file
        save_users(users)

        st.success("Profile saved successfully")

# career section
elif selected == 'Career':
    st.subheader("Career Info")
 
    career = st.session_state.get("career", {})

    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Current Role", value=career.get("role"))
    with col2:
        company = st.text_input("Company", value=career.get("company"))

    experience_level = st.selectbox("Experience", [
        "0-2", "3-5", "6-10", "10+"
    ])

    col1, col2, col3 = st.columns(3)
    with col1:
        github = st.text_input("GitHub", value=career.get("github"))
    with col2:
        linkedin = st.text_input("LinkedIn", value=career.get("linkedin"))
    with col3:
        website = st.text_input("Website", value=career.get("website"))

    if st.button(":material/save: Save Changes", key='career-save-btn'):

        st.session_state.career = {
            "role": role,
            "company": company,
            "experience": experience_level,
            "github": github,
            "linkedin": linkedin,
            "website": website
        }

        users = load_users()

        for u in users:
            if u["email"] == st.session_state.user["email"]:
                u["career"] = st.session_state.career

        save_users(users)

        st.success("Career saved successfully")


# notifications section

elif selected == 'Notifications':
    st.subheader("Notifications")

    st.toggle("Email Notifications", True)
    st.toggle("Push Notifications", True)
    st.toggle("Interview Reminders", True)
    st.toggle("Weekly Reports", False)

    if st.button("Save Preferences"):
        st.success("Saved")

# Privacy section
elif selected == 'Privacy':
    st.subheader("Privacy")

    st.selectbox("Profile Visibility", [
        "Public", "Private", "Connections"
    ])

    st.toggle("Share Progress", True)
    st.toggle("Allow Messages", True)

    if st.button("Save Settings"):
        st.success("Saved")

# Achievements section

elif selected == 'Achievements':
    st.subheader("Achievements")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✅ First Interview Completed")
        st.info("⭐ Communication Pro")

    with col2:
        st.warning("🔒 Perfect Score Locked")
        st.warning("🔒 Technical Expert Locked")