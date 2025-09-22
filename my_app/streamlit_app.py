# streamlit_app.py
import streamlit as st
from streamlit_option_menu import option_menu
st.set_page_config(
    page_title="⚖️ Legal Aid Advisor - LegiSense",
    layout="wide",
    initial_sidebar_state="auto"
)

# Add pages folder to path
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "pages"))

# Import modules
import home
import legal_chatbot
import legal_affidavit
import legal_rti
import legal_dispute
import summarizer
import register_lawyer
import find_lawyer




# ---------- Top Navigation ----------
selected = option_menu(
    menu_title=None,  # no title
    options=[
        "Home",
        "Chatbot",
        "Affidavit Generator",
        "RTI & Customer Dispute",
        "Legal Summarizer",
        "Register/Find Lawyers"   # 👈 NEW MENU OPTION
    ],
    icons=[
        "house",
        "robot",
        "file-text",
        "file-earmark-text",
        "book-open",
        "people-fill"   # 👈 Bootstrap icon for lawyers
    ],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# ---------- Display Pages ----------
if selected == "Home":
    home.show_home()

elif selected == "Chatbot":
    legal_chatbot.show_chatbot()

elif selected == "Affidavit Generator":
    legal_affidavit.show_affidavit_page()

elif selected == "RTI & Customer Dispute":
    tab = st.radio("📌 Choose Document Type:", ["RTI Application", "Customer Dispute"])
    if tab == "RTI Application":
        legal_rti.show_rti_page()
    else:
        legal_dispute.show_dispute_page()

elif selected == "Legal Summarizer":
    summarizer.show_legal_summarizer()

elif selected == "Register/Find Lawyers":
    tab = st.radio("📌 Choose :", ["Register", "Search"])
    if tab == "Register":
        register_lawyer.show_register_lawyer()   # ✅ fixed
    else:
        find_lawyer.show_find_lawyer()           # ✅ fixed
