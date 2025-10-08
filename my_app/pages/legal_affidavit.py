# pages/affidavit.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile
import datetime

# --- 1. TEMPLATE AND GENERATION LOGIC (Unchanged) ---
affidavit_template = """
AFFIDAVIT

STATE OF {{ state }} COUNTY OF {{ county }}

{{ name }}, being first duly sworn, hereby declares and affirms as follows:

I. Introduction

My name is {{ name }}.
I am a {{ nationality }}.
My address is {{ address }}.

II. Statement of Facts

{{ facts }}

III. Jurat

I do solemnly swear that the foregoing statements are true and correct to the best of my knowledge and belief.

IV. Signature

Signed on {{ date }} at {{ city }}, {{ state }} before me:

Your Signature: _________________________

V. Notary Public's Information

My commission expires: {{ commission_expiry }};
I am a notary public for the State of {{ state }};
My notary public number is: {{ notary_number }}.

VI. Certificate of Acknowledgment

The foregoing instrument was acknowledged by {{ name }} on this day, {{ date }}, in my presence.

[Notary Public's Signature] _________________________
"""

def generate_affidavit(user_data):
    template = Template(affidavit_template)
    return template.render(user_data)


# --- 2. REDESIGNED STREAMLIT UI FUNCTION ---
def show_affidavit_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>📝 Affidavit Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Fill in the details below to generate a formal affidavit. Your document will be available for preview and download.</p>", unsafe_allow_html=True)
    st.divider()

    # --- INPUT FORM WITH TWO-COLUMN LAYOUT FOR FIELDS ---
    st.subheader("1. Enter Affidavit Details")

    with st.container(border=True):
        with st.expander("👤 **Deponent's Information**", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", key="aff_name")
            with col2:
                nationality = st.text_input("Nationality", "citizen of India", key="aff_nationality")
            address = st.text_area("Full Address", height=100, key="aff_address")

        with st.expander("📍 **Jurisdiction Information**", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                state = st.text_input("State", key="aff_state")
            with col2:
                county = st.text_input("County / District", key="aff_county")
            city = st.text_input("City", key="aff_city")

        with st.expander("⚖️ **Statement of Facts**", expanded=True):
            facts = st.text_area("Provide the facts you are swearing to", height=150, help="Clearly state the facts.", key="aff_facts")

        with st.expander("✒️ **Notary & Signing Details**", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                date_val = st.date_input("Date of Signing", datetime.date.today(), key="aff_date")
            with col2:
                commission_expiry = st.text_input("Notary Commission Expiry Date", key="aff_expiry")
            notary_number = st.text_input("Notary Public Number", key="aff_notary_num")

    # --- GENERATE BUTTON ---
    if st.button("✨ Generate Affidavit & Preview", use_container_width=True, type="primary"):
        if not all([name, address, state, county, city, facts]):
            st.warning("Please fill in all required fields before generating.")
        else:
            date_str = date_val.strftime("%d %B %Y")
            user_data = {
                "name": name, "nationality": nationality, "state": state,
                "county": county, "city": city, "address": address, "facts": facts,
                "date": date_str, "commission_expiry": commission_expiry,
                "notary_number": notary_number
            }
            st.session_state['affidavit_text'] = generate_affidavit(user_data)
            st.session_state['user_data'] = user_data

    # --- OUTPUT SECTION (PREVIEW & DOWNLOAD) ---
    if 'affidavit_text' in st.session_state:
        st.divider()
        st.subheader("2. Preview and Download")
        
        affidavit_text = st.session_state['affidavit_text']
        
        # Display the preview
        st.text_area("Document Preview", affidavit_text, height=400)

        # --- PDF GENERATION USING THE ROBUST pdf.write() METHOD (as provided) ---
        user_data = st.session_state['user_data']
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        line_height = 6

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "AFFIDAVIT", align='C')
        pdf.ln(20)

        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, f"STATE OF {user_data['state']} COUNTY OF {user_data['county']}\n\n")
        pdf.write(line_height, f"{user_data['name']}, being first duly sworn, hereby declares and affirms as follows:\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "I. Introduction\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, f"My name is {user_data['name']}.\n")
        pdf.write(line_height, f"I am a {user_data['nationality']}.\n")
        pdf.write(line_height, f"My address is {user_data['address']}.\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "II. Statement of Facts\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, user_data['facts'] + "\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "III. Jurat\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, "I do solemnly swear that the foregoing statements are true and correct to the best of my knowledge and belief.\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "IV. Signature\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, f"Signed on {user_data['date']} at {user_data['city']}, {user_data['state']} before me:\n\n\n")
        pdf.write(line_height, "Your Signature: _________________________\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "V. Notary Public's Information\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, f"My commission expires: {user_data['commission_expiry']};\n")
        pdf.write(line_height, f"I am a notary public for the State of {user_data['state']};\n")
        pdf.write(line_height, f"My notary public number is: {user_data['notary_number']}.\n\n")

        pdf.set_font("Arial", "B", 12)
        pdf.write(line_height, "VI. Certificate of Acknowledgment\n")
        pdf.set_font("Arial", "", 12)
        pdf.write(line_height, f"The foregoing instrument was acknowledged by {name} on this day, {user_data['date']}, in my presence.\n\n\n")
        pdf.write(line_height, "[Notary Public's Signature] _________________________")
        
        # Save to a temporary file for downloading
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf_file_path = tmp.name
            pdf.output(pdf_file_path)
        
        with open(pdf_file_path, "rb") as f:
            pdf_bytes = f.read()

        st.download_button(
            label="⬇️ Download Affidavit as PDF",
            data=pdf_bytes,
            file_name="Affidavit.pdf",
            mime="application/pdf",
            use_container_width=True
        )