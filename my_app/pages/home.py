# pages/Home.py
import streamlit as st

def show_home():
    st.title("⚖️ Legisense")
    
    st.write("""
    Welcome to the **Legisense** platform!  

    This platform helps you:
    - Generate legal documents like **Affidavits**, **RTI Applications**, and **Customer Dispute Letters**.
    - Ask legal questions through our **interactive chatbot**.
    - Access tools easily through the **topbar navigation**.
    """)
    
    st.subheader("Getting Started")
    st.write("""
    1. Use the topbar in the center to navigate between tools.
    2. Fill out the forms on each page to generate legal documents.
    3. Download your generated PDF and submit/sign as required.
    4. Chat with the chatbot for guidance or clarifications on legal processes.
    """)
    
    st.info("This platform is for **informational purposes** and does not replace professional legal advice.")
    
    # Optional: add links to resources or examples
    st.subheader("Resources")
    st.markdown("- [Legal Document Guidelines](https://www.indiacode.nic.in/)")
    st.markdown("- [RTI Act Information](https://rti.gov.in/)")
