# streamlit_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import os
import sys
import subprocess
import time

# Import DB functions for Auth
from database.db import init_db, verify_login, create_user

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="⚖️ Legal Aid Advisor - LegalEase",
    layout="wide",
    initial_sidebar_state="expanded"
)
def inject_global_css():
    st.markdown("""
        <style>
            /* 1. Hide the native file navigation list globally */
            [data-testid="stSidebarNav"] {
                display: none !important;
            }
            
            /* 2. Ensure the sidebar toggle button remains accessible */
            [data-testid="stHeader"] {
                background-color: transparent !important;
            }
        </style>
    """, unsafe_allow_html=True)

# Call it once here
inject_global_css()

# Initialize DB
init_db()

# --- 2. SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = ""

# --- 3. BROWSER INSTALLATION (For Summarizer) ---
@st.cache_resource
def install_playwright_browser():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
    except Exception as e:
        st.error(f"Playwright Browser Installation failed: {e}")

install_playwright_browser()

# --- 4. SIDEBAR AUTHENTICATION ---
with st.sidebar:
    st.title("⚖️ LegalEase")
    
    # If User is NOT Logged In -> Show Login/Signup Forms
    if not st.session_state['logged_in']:
        st.info("🔒 Please Login to access tools")
        auth_mode = st.radio("Choose Option:", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
        
        if auth_mode == "Login":
            with st.form("sidebar_login"):
                user = st.text_input("Username")
                pwd = st.text_input("Password", type="password")
                btn = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if btn:
                    role = verify_login(user, pwd)
                    if role:
                        st.session_state['logged_in'] = True
                        st.session_state['role'] = role
                        st.session_state['username'] = user
                        st.success(f"Welcome, {user}!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

        elif auth_mode == "Sign Up":
            with st.form("sidebar_signup"):
                new_user = st.text_input("New Username")
                new_pwd = st.text_input("New Password", type="password")
                btn_sign = st.form_submit_button("Create Account", use_container_width=True)
                
                if btn_sign:
                    if len(new_pwd) < 4:
                        st.error("Password too short!")
                    elif create_user(new_user, new_pwd):
                        st.success("Account created! Please switch to Login.")
                    else:
                        st.error("Username taken.")

    # If User IS Logged In -> Show User Info & Logout
    else:
        st.success(f"👤 Logged in as: **{st.session_state['username']}**")
        if st.session_state['role'] == 'admin':
            st.info("🔧 Admin Privileges Active")
        
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['role'] = None
            st.session_state['username'] = ""
            st.rerun()
            
    st.divider()
    st.markdown("Your AI-Powered Legal Assistant")

# --- 5. IMPORT PAGE MODULES ---
sys.path.append(os.path.join(os.path.dirname(__file__), "pages"))
import home
import legal_chatbot
import summarizer
import legal_affidavit
import legal_rti
import legal_dispute
import register_lawyer
import find_lawyer
import admin

# --- 6. NAVIGATION MENU ---
# Standard Menu for Everyone
menu_options = ["Home", "AI Chatbot", "Summarizer", "Affidavit", "RTI / Dispute", "Lawyers"]
menu_icons = ["house-door-fill", "chat-dots-fill", "card-text", "file-earmark-richtext-fill", "journal-richtext", "people-fill"]

# Add Admin Option ONLY if Logged in as Admin
if st.session_state['logged_in'] and st.session_state['role'] == 'admin':
    menu_options.append("Admin")
    menu_icons.append("wrench-adjustable-circle-fill")

selected = option_menu(
    menu_title=None,
    options=menu_options,
    icons=menu_icons,
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#F0F2F6", "border-radius": "10px"},
        "icon": {"color": "#31333F", "font-size": "16px"},
        "nav-link": {
            "font-size": "14px", "font-weight": "600", "color": "#31333F", 
            "text-align": "center", "margin": "0px", "--hover-color": "#E1E8F0", 
            "padding": "10px 12px"
        },
        "nav-link-selected": {"background-color": "#004AAD", "color": "white"},
    }
)

# --- 7. PAGE ROUTING WITH ACCESS CONTROL ---

# Helper function to block access
def check_access():
    if not st.session_state['logged_in']:
        st.warning("🔒 **Access Restricted**")
        st.info("Please **Login** or **Sign Up** using the sidebar on the left to access this tool.")
        st.stop() # Stops the rest of the page from loading

if selected == "Home":
    # Home is ALWAYS public
    home.show_home()

elif selected == "AI Chatbot":
    check_access() # 🔒
    legal_chatbot.show_chatbot()

elif selected == "Summarizer":
    check_access() # 🔒
    summarizer.show_legal_summarizer()

elif selected == "Affidavit":
    check_access() # 🔒
    legal_affidavit.show_affidavit_page()

elif selected == "RTI / Dispute":
    check_access() # 🔒
    tab1, tab2 = st.tabs(["RTI Application", "Customer Dispute"])
    with tab1: legal_rti.show_rti_page()
    with tab2: legal_dispute.show_dispute_page()

elif selected == "Lawyers":
    check_access() # 🔒
    tab1, tab2 = st.tabs(["Register as a Lawyer", "Find a Lawyer"])
    with tab1: register_lawyer.show_register_lawyer()
    with tab2: find_lawyer.show_find_lawyer()

elif selected == "Admin":
    # Double check security
    if st.session_state['role'] == 'admin':
        admin.show_admin_page()
    else:
        st.error("⛔ Access Denied.")