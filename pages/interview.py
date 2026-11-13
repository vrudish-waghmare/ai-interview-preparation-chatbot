import streamlit as st
from utils.evaluator import evaluate_answer
from utils.adaptive import generate_followup
from utils.questions import get_question
from utils.session import require_login

st.set_page_config(layout="wide")


# Auto login from cookie
require_login()



# Login Config
config = st.session_state.get("config", {})

# Debug: Check if config is empty
if not config or not config.get("role"):
    st.error("❌ Interview config not set. Please complete setup on the home page first.")
    st.stop()

profile = config.get("profile", {})
role = config.get("role", "Software Engineer")
difficulty = config.get("difficulty", "Beginner")
skills = config.get("skills", [])
duration = config.get("duration", 30)

# Map duration to question limit
QUESTION_LIMIT = {
    15: 3,
    30: 5,
    45: 7,
    60: 10
}

limit = QUESTION_LIMIT.get(duration, 5)


# Initalize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "total_score" not in st.session_state:
    st.session_state.total_score = 0

if "q_index" not in st.session_state:
    st.session_state.q_index = 0



config_hash = st.session_state.get("_config_hash")
try:
    new_hash = hash(frozenset(config.items()))
except Exception:
    new_hash = None

if ("current_question" not in st.session_state) or (config_hash != new_hash):
    st.session_state["_config_hash"] = new_hash

    if profile.get("bio"):
        first_q = f"Based on your background: {profile.get('bio')}, tell me about your experience relevant to {role}."
    else:
        first_q = get_question(role) or f"Tell me about your experience relevant to {role}."

    st.session_state.current_question = first_q
    st.session_state.messages.append({
        "role": "assistant",
        "content": first_q
    })
    

# Check if interview is complete BEFORE showing UI
if st.session_state.q_index >= limit:
    st.success("🎉 Interview Complete!")
    st.info("Redirecting to report page...")
    st.switch_page("pages/report.py")
    st.stop()


# UI
st.title("🎤 AI Interview")

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat Input
user_input = st.chat_input("Type your answer...")

if user_input:
    
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

   
   # Evaluate answer
    with st.spinner("Evaluating..."):
        result = evaluate_answer(
            st.session_state.current_question,
            user_input
        )

    score = result.get("score", 5)
    skills_score = result.get("skills", {})

    
    # Build feedback
    feedback_msg = f"""
**Score: {score}/10**

### 🧠 Skill Breakdown
- Communication: {skills_score.get("communication", 0)}/10
- Technical: {skills_score.get("technical", 0)}/10
- Clarity: {skills_score.get("clarity", 0)}/10
- Problem Solving: {skills_score.get("problem_solving", 0)}/10

### ✅ Strengths
{chr(10).join(f"- {s}" for s in result.get("strengths", []))}

### ❌ Weaknesses
{chr(10).join(f"- {w}" for w in result.get("weaknesses", []))}

### 📌 Missing Concepts
{chr(10).join(f"- {m}" for m in result.get("missing_concepts", []))}
"""

    # Store score + history
    st.session_state.total_score += score

    st.session_state.history.append({
        "question": st.session_state.current_question,
        "answer": user_input,
        "score": score,
        "skills": skills_score,
        "strengths": result.get("strengths", []),
        "weaknesses": result.get("weaknesses", []),
        "missing_concepts": result.get("missing_concepts", [])
    })

   ## show assistance feedback
    st.session_state.messages.append({
        "role": "assistant",
        "content": feedback_msg
    })

    with st.chat_message("assistant"):
        st.markdown(feedback_msg)

    
    # next question
    st.session_state.q_index += 1

    if st.session_state.q_index >= limit:
        st.switch_page("pages/report.py")

    else:
        with st.spinner("Thinking..."):
            followup = generate_followup(
                st.session_state.current_question,
                user_input,
                feedback_msg,
                role,
                difficulty,
                skills,
                profile
            )

        if not followup:
            followup = get_question(role)

        st.session_state.current_question = followup

        st.session_state.messages.append({
            "role": "assistant",
            "content": followup
        })

        st.rerun()