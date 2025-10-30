# streamlit_app.py
import streamlit as st
from streamlit_option_menu import option_menu

# Add pages folder to path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "pages"))

# Import your page modules
import home
import legal_chatbot
import summarizer
import legal_affidavit
import legal_rti
import legal_dispute
import register_lawyer
import find_lawyer
import admin


# Page configuration
st.set_page_config(
    page_title="⚖️ Legal Aid Advisor - LegalEase",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLED NAVIGATION MENU (MORE COMPACT) ---
selected = option_menu(
    menu_title=None,
    options=[
        "Home",
        "AI Chatbot",
        "Summarizer",
        "Affidavit",
        "RTI / Dispute",
        "Lawyers",
        "Admin"
    ],
    icons=[
        "house-door-fill",
        "chat-dots-fill",
        "card-text",
        "file-earmark-richtext-fill",
        "journal-richtext",
        "people-fill",
        "wrench-adjustable-circle-fill"
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#F0F2F6", "border-radius": "10px"},
        "icon": {
            "color": "#31333F",
            "font-size": "16px"  
        },
        "nav-link": {
            "font-size": "14px",  
            "font-weight": "600",
            "color": "#31333F",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#E1E8F0",
            "padding": "10px 12px" 
        },
        "nav-link-selected": {
            "background-color": "#004AAD",
            "color": "white"
        },
    }
)

# --- PAGE DISPLAY LOGIC ---
if selected == "Home":
    home.show_home()
elif selected == "AI Chatbot":
    legal_chatbot.show_chatbot()
elif selected == "Summarizer":
    summarizer.show_legal_summarizer()
elif selected == "Affidavit":
    legal_affidavit.show_affidavit_page()
elif selected == "RTI / Dispute":
    tab1, tab2 = st.tabs(["RTI Application", "Customer Dispute"])
    with tab1:
        legal_rti.show_rti_page()
    with tab2:
        legal_dispute.show_dispute_page()
elif selected == "Lawyers":
    tab1, tab2 = st.tabs(["Register as a Lawyer", "Find a Lawyer"])
    with tab1:
        register_lawyer.show_register_lawyer()
    with tab2:
        find_lawyer.show_find_lawyer()
elif selected == "Admin":
    admin.show_admin_page()