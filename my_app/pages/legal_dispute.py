# pages/dispute.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile

dispute_template = """
TO  
The Manager / Customer Service Officer  
{{ company_name }}  
{{ company_address }}  

Subject: Complaint / Dispute Regarding {{ product_service }}

Dear Sir/Madam,

I, {{ complainant_name }}, residing at {{ complainant_address }}, am writing to formally lodge a complaint regarding {{ product_service }}.

Details of the issue:
{{ issue_details }}

I request the following resolution:
{{ desired_resolution }}

I hope this matter will be resolved promptly as per your company policies and applicable laws.

Thank you.

Date: {{ date }}  
Place: {{ complainant_address }}  

Sincerely,  
{{ complainant_name }}
"""

def generate_dispute(user_data):
    template = Template(dispute_template)
    return template.render(user_data)


def show_dispute_page():
    st.title("📄 Customer Dispute / Complaint Letter Generator")

    # Step 1: Collect user inputs
    complainant_name = st.text_input("Enter your full name")
    complainant_address = st.text_area("Enter your address")
    company_name = st.text_input("Enter the company/organization name")
    company_address = st.text_area("Enter the company address")
    product_service = st.text_input("Product or Service related to the dispute")
    issue_details = st.text_area("Describe the issue or dispute in detail")
    desired_resolution = st.text_area("Desired resolution or action")
    date = st.date_input("Enter date of complaint")

    # Step 2: Generate dispute letter
    if st.button("Generate Complaint Letter"):
        user_data = {
            "complainant_name": complainant_name,
            "complainant_address": complainant_address,
            "company_name": company_name,
            "company_address": company_address,
            "product_service": product_service,
            "issue_details": issue_details,
            "desired_resolution": desired_resolution,
            "date": date.strftime("%d %B %Y")
        }

        dispute_text = generate_dispute(user_data)
        st.subheader("Generated Complaint / Dispute Letter")
        st.text_area("Complaint Letter", dispute_text, height=400)

        # Convert to PDF with bold headings & key fields
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        headings = ["TO", "Subject", "Dear Sir/Madam,", "Thank you.", "Sincerely,"]
        bold_words = [complainant_name, complainant_address, company_name, company_address, product_service]

        for line in dispute_text.split("\n"):
            if any(line.strip().startswith(h) for h in headings):
                pdf.set_font("Arial", "B", 12)
            elif any(word in line for word in bold_words):
                pdf.set_font("Arial", "B", 12)
            else:
                pdf.set_font("Arial", "", 12)

            pdf.multi_cell(0, 6, line)

        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(temp_file.name)

        st.download_button(
            label="Download Complaint as PDF",
            data=open(temp_file.name, "rb").read(),
            file_name="Customer_Dispute.pdf",
            mime="application/pdf"
        )
