import streamlit as st
from utils.cookies import get_cookie, delete_cookie
from utils.auth import clear_session
from utils.session import require_login
from utils.logout_btn import logout_button, logout_confirmation_modal

st.set_page_config(
    page_title = "AI Interview Chatbot",
    page_icon = 'assets/logo.svg', 
    layout="wide",
    initial_sidebar_state = "expanded" 
)

with st.sidebar:
    st.title("AI Interview ChatBot")

# auto login
require_login()

# login before entering
if "user" not in st.session_state:
    st.warning("Please login first")
    st.stop()

profile = st.session_state.get("profile", {})
career = st.session_state.get("career", {})

# header section
with st.container():
    col1, col2 = st.columns([8, 2])
    with col2:
        logout_button()

    st.subheader("🎤 Interview Setup")
    st.write("Configure your AI-powered interview session")

# logout
logout_confirmation_modal()

# main layout
left_column, right_column = st.columns([3, 1], gap="large")

with left_column:

    with st.container(border=True):
        st.markdown("### ⚙️ Basic Information")

        col1, col2 = st.columns(2)

        with col1:
            default_role = career.get("role")

            role = st.selectbox(
                "Target Role",
                ["Software Engineer", "Data Scientist", "Product Manager"],
                index=(
                    ["Software Engineer", "Data Scientist", "Product Manager"].index(default_role)
                    if default_role in ["Software Engineer", "Data Scientist", "Product Manager"]
                    else None
                ),
                placeholder="Select role"
            )

        with col2:
            company = st.selectbox(
                "Company Type",
                ["Big Tech", "Startup", "Enterprise"],
                index=None,
                placeholder="Select company"
            )

            context = st.text_area(
                "Additional Context",
                placeholder="Technologies, topics, etc..."
            )

    with st.container(border=True):
        st.markdown("### 🧠 Interview Type")

        types = ["Behavioral", "Technical", "System Design", "Case Study", "Mixed"]

        selected_type = st.radio(
            "Select Type",
            types,
            horizontal=True
        )

    with st.container(border=True):
        st.markdown("### 🎯 Focus Areas")

        skills = st.multiselect(
            "Skills",
            [
                "Communication",
                "Problem Solving",
                "Technical Depth",
                "Leadership",
                "Creativity"
            ]
        )

with right_column:

    with st.container(border=True):
        st.markdown("### ⏱ Settings")

        duration = st.select_slider(
            "Duration (minutes)",
            [15, 30, 45, 60],
            value=30
        )

        difficulty = st.select_slider(
            "Difficulty",
            ["Beginner", "Intermediate", "Expert"],
            value="Beginner"
        )

        realtime_feedback = st.toggle("Real-time Feedback", value=True)

# start button
    with st.container(border=True):

        start = st.button("🚀 Start Interview", use_container_width=True)

        if start:
            if not role or not company:
                st.error("Please select role and company before starting.")
                st.stop()

            # Only reset interview-related state
            st.session_state.q_index = 0
            st.session_state.messages = []
            st.session_state.history = []
            st.session_state.total_score = 0

            # Store config
            st.session_state.config = {
                "role": role,
                "company": company,
                "context": context,
                "type": selected_type,
                "skills": skills,
                "duration": duration,
                "difficulty": difficulty,
                "realtime": realtime_feedback,
                "profile": st.session_state.get("profile", {}),
                "career": st.session_state.get("career", {})
            }

            st.session_state.q_index = 0
            st.session_state.messages = []
            st.session_state.history = []
            st.session_state.total_score = 0

            st.switch_page("pages/interview.py")

        st.info("Make sure you're in a quiet place before starting.")