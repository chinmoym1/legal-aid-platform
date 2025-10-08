# pages/Home.py
import streamlit as st

def show_home():
    # --- PAGE CONFIGURATION ---
    # Ensure this is set in your main app script for consistency
    # st.set_page_config(layout="wide", page_title="LegalEase AI", page_icon="⚖️")

    # --- CUSTOM CSS FOR STYLING ---
    # We'll inject CSS to style our elements for a more professional look
    st.markdown("""
        <style>
            /* Main title */
            .main-title {
                color: #004AAD; /* Primary Blue */
                text-align: center;
                font-size: 3em;
                font-weight: bold;
            }
            /* Subtitle */
            .subtitle {
                color: #31333F; /* Charcoal Text */
                text-align: center;
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            /* Feature Cards */
            .card {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform 0.2s;
                height: 100%;
            }
            .card:hover {
                transform: scale(1.05);
            }
            .card-icon {
                font-size: 3em;
                margin-bottom: 15px;
            }
            .card-title {
                color: #004AAD; /* Primary Blue */
                font-size: 1.5em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .card-text {
                color: #31333F; /* Charcoal Text */
                font-size: 1em;
            }
            /* How it works section */
            .step-number {
                background-color: #004AAD;
                color: white;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                display: inline-block;
                line-height: 40px;
                font-size: 1.5em;
                font-weight: bold;
                text-align: center;
                margin-bottom: 15px;
            }
            .step-title {
                font-weight: bold;
                font-size: 1.2em;
                color: #31333F;
            }
            /* Disclaimer Box */
            .disclaimer {
                background-color: #FFFBEB; /* Light yellow */
                border-left: 5px solid #FBBF24; /* Amber/Gold */
                padding: 15px;
                border-radius: 5px;
                margin-top: 30px;
            }
        </style>
    """, unsafe_allow_html=True)

    # --- HERO SECTION ---
    st.markdown('<h1 class="main-title">⚖️Welcome to LegalEase AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your AI-Powered Legal Assistant for Document Generation and Guidance</p>', unsafe_allow_html=True)
    st.divider()

    # --- FEATURE CARDS SECTION ---
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
            <div class="card">
                <div class="card-icon">📄</div>
                <div class="card-title">Document Generators</div>
                <div class="card-text">Quickly generate standardized legal documents like Affidavits, RTI Applications, and Customer Complaints. Just fill out a simple form.</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="card">
                <div class="card-icon">🤖</div>
                <div class="card-title">AI Legal Chatbot</div>
                <div class="card-text">Have a legal question? Our interactive chatbot provides preliminary information and guidance on a variety of legal topics.</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="card">
                <div class="card-icon">📑</div>
                <div class="card-title">AI Legal Summarizer</div>
                <div class="card-text">Upload complex legal documents like judgments or contracts, and our AI will provide a simple, easy-to-understand summary.</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("") # Spacer
    st.divider()

    # --- HOW IT WORKS SECTION ---
    st.markdown('<h2 style="text-align: center; color: #004AAD;">How It Works</h2>', unsafe_allow_html=True)
    st.write("") # Spacer

    step1, step2, step3 = st.columns(3, gap="large")
    with step1:
        st.markdown("""
            <div style="text-align: center;">
                <div class="step-number">1</div>
                <div class="step-title">Select a Tool</div>
                <p>Choose a generator or AI assistant from the navigation sidebar.</p>
            </div>
        """, unsafe_allow_html=True)
    with step2:
        st.markdown("""
            <div style="text-align: center;">
                <div class="step-number">2</div>
                <div class="step-title">Provide Details</div>
                <p>Fill in the required information in our user-friendly forms.</p>
            </div>
        """, unsafe_allow_html=True)
    with step3:
        st.markdown("""
            <div style="text-align: center;">
                <div class="step-number">3</div>
                <div class="step-title">Generate & Download</div>
                <p>Instantly create and download your document as a PDF, ready for use.</p>
            </div>
        """, unsafe_allow_html=True)

    # --- DISCLAIMER ---
    st.markdown("""
        <div class="disclaimer">
            <b>Disclaimer:</b> This platform is intended for informational purposes only and does not constitute professional legal advice. Always consult with a qualified legal professional for your specific situation.
        </div>
    """, unsafe_allow_html=True)