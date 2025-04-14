# Dummy authentication functions for Streamlit app
import streamlit as st

def register_user(username, email, password):
    """Dummy register function"""
    st.session_state.is_authenticated = True
    st.session_state.username = username
    st.session_state.user_id = 1  # Set a dummy user_id
    return True, ""

def login_user(username, password):
    """Dummy login function"""
    st.session_state.is_authenticated = True
    st.session_state.username = username
    st.session_state.user_id = 1  # Set a dummy user_id
    return True, ""

def logout_user():
    """Dummy logout function"""
    if 'is_authenticated' in st.session_state:
        del st.session_state.is_authenticated
    if 'username' in st.session_state:
        del st.session_state.username
    if 'user_id' in st.session_state:
        del st.session_state.user_id
    st.rerun()

def verify_email(token):
    """Dummy verify email function"""
    return True, ""

def request_password_reset(email):
    """Dummy password reset request function"""
    return True, ""

def reset_password(token, new_password):
    """Dummy reset password function"""
    return True, ""

def update_user_preferences(user_id, language=None, theme=None, notifications=None):
    """Dummy update preferences function"""
    if language is not None:
        st.session_state.language = language
    return True, ""

def log_user_activity(user_id, action, details=None, ip_address=None, user_agent=None):
    """Dummy log activity function"""
    return True

def get_user_activity_logs(user_id, limit=10):
    """Dummy get activity logs function"""
    return []

def is_valid_email(email):
    """Dummy email validation function"""
    return True

def generate_token():
    """Dummy token generation function"""
    return "dummy_token"
