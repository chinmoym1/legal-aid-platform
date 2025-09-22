# pages/affidavit.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile

# Affidavit template
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

Your Signature:



V. Notary Public's Information

My commission expires: {{ commission_expiry }};
I am a notary public for the State of {{ state }};
My notary public number is: {{ notary_number }}.

VI. Certificate of Acknowledgment

The foregoing instrument was acknowledged by {{ name }} on this day, {{ date }}, in my presence.

[Notary Public's Signature]
"""

# Generate text using Jinja2
def generate_affidavit(user_data):
    template = Template(affidavit_template)
    return template.render(user_data)


def show_affidavit_page():
    st.title("📝 Affidavit Generator")

    # Step 1: Collect user inputs
    name = st.text_input("Enter your full name")
    nationality = st.text_input("Enter your nationality", "citizen of India")
    state = st.text_input("Enter your state")
    county = st.text_input("Enter your county/district")
    city = st.text_input("Enter your city")
    address = st.text_area("Enter your address")
    facts = st.text_area("Enter the facts you want to state")
    date = st.date_input("Enter date of signing")
    commission_expiry = st.text_input("Enter notary commission expiry date")
    notary_number = st.text_input("Enter notary public number")

    # Step 2: Generate affidavit
    if st.button("Generate Affidavit"):
        user_data = {
            "name": name,
            "nationality": nationality,
            "state": state,
            "county": county,
            "city": city,
            "address": address,
            "facts": facts,
            "date": date.strftime("%d %B %Y"),
            "commission_expiry": commission_expiry,
            "notary_number": notary_number
        }

        affidavit_text = generate_affidavit(user_data)
        st.subheader("Generated Affidavit")
        st.text_area("Affidavit", affidavit_text, height=400)

        # Convert to PDF with bold headings & user fields
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Define headings and user fields to bold
        headings = [
            "AFFIDAVIT", "I. Introduction", "II. Statement of Facts",
            "III. Jurat", "IV. Signature", "V. Notary Public's Information",
            "VI. Certificate of Acknowledgment"
        ]
        bold_words = [name, address, facts]

        for line in affidavit_text.split("\n"):
            # Bold headings
            if line.strip() in headings:
                pdf.set_font("Arial", "B", 12)
            # Bold user-specific content
            elif any(word in line for word in bold_words):
                pdf.set_font("Arial", "B", 12)
            else:
                pdf.set_font("Arial", "", 12)

            pdf.multi_cell(0, 6, line)

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)

        st.download_button(
            label="Download Affidavit as PDF",
            data=open(temp_file.name, "rb").read(),
            file_name="affidavit.pdf",
            mime="application/pdf"
        )
