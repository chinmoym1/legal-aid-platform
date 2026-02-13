# pages/auth.py
import streamlit as st
from database.db import verify_login, create_user
import time

def show_login_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>🔐 Login to LegalEase</h1>", unsafe_allow_html=True)
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Toggle between Login and Signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        # --- LOGIN TAB ---
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", type="primary", use_container_width=True)

                if submit:
                    role = verify_login(username, password)
                    if role:
                        st.success(f"Welcome back, {username}!")
                        # Save session state
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['role'] = role
                        time.sleep(1)
                        st.rerun() # Refresh to show the app
                    else:
                        st.error("Invalid username or password.")

        # --- SIGNUP TAB ---
        with tab2:
            with st.form("signup_form"):
                new_user = st.text_input("New Username")
                new_pass = st.text_input("New Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submit_signup = st.form_submit_button("Create Account", use_container_width=True)

                if submit_signup:
                    if new_pass != confirm_pass:
                        st.error("Passwords do not match!")
                    elif len(new_pass) < 4:
                        st.error("Password must be at least 4 characters.")
                    else:
                        if create_user(new_user, new_pass):
                            st.success("Account created! You can now log in.")
                        else:
                            st.error("Username already exists. Please choose another.")