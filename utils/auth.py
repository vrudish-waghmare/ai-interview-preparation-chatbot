import streamlit as st 
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from utils.cookies import delete_cookie


DB_PATH = "data/users.json"
SESSION_PATH = "data/session.json"

# file helpers
def load_users():
    if not os.path.exists(DB_PATH):
        return []

    try:
        with open(DB_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def save_users(users):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)


#authorization functions
def create_user(email, password, first_name, last_name):
    users = load_users()

    if any(u["email"] == email for u in users):
        return False, "User already exists"

    user = {
        "email": email,
        "password": generate_password_hash(password),  
        "profile": {
            "first_name": first_name,
            "last_name": last_name,
        },
        "career": {}
    }

    users.append(user)
    save_users(users)

    return True, user


def login_user(email, password):
    users = load_users()

    for user in users:
        if user["email"] == email and check_password_hash(user["password"], password):
            return True, user

    return False, "Invalid credentials"


# session functions
def is_logged_in():
    return "user" in st.session_state


def logout_user():
    """
    Complete logout process with proper state cleanup
    Prevents re-authentication without fresh login
    """
    try:
        delete_cookie("user_email")
    except Exception as e:
        print(f"❌ Cookie deletion error: {e}")
    
    try:
        clear_session()
    except Exception as e:
        print(f"❌ Session clear error: {e}")
    
    try:
        # Explicitly set user to None and clear related state
        st.session_state.user = None
        st.session_state.profile = None
        st.session_state.career = None
        st.session_state.config = None
        
        # Clear all other session keys except logout flag
        keys_to_keep = ["is_logged_out"]
        for key in list(st.session_state.keys()):
            if key not in keys_to_keep:
                try:
                    del st.session_state[key]
                except:
                    pass
    except Exception as e:
        print(f"❌ Session state error: {e}")


# Update helpers
def update_user_data(email, key, value):
    users = load_users()

    for u in users:
        if u["email"] == email:
            u[key] = value
            save_users(users)
            return True

    return False


# Session file helpers
def save_session(email):
    os.makedirs("data", exist_ok=True)

    with open(SESSION_PATH, "w") as f:
        json.dump({"email": email}, f)


def load_session():
    if not os.path.exists(SESSION_PATH):
        return None
    try:
        with open(SESSION_PATH, "r") as f:
            data = json.load(f) 
            return data.get("email")
    except:
        return None


def clear_session():
    if os.path.exists(SESSION_PATH):
        os.remove(SESSION_PATH)