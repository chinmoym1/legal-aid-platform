# RTI.py
# pages/rti.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile

rti_template = """
TO  
The Public Information Officer  
{{ public_authority }}  

Subject: Request for information under the RTI Act, 2005  

Dear Sir/Madam,

I, {{ applicant_name }}, residing at {{ applicant_address }}, hereby request the following information under the Right to Information Act, 2005:

{{ information_details }}

The subject of this request is: {{ subject }}.

I am enclosing the required application fee (if applicable) and request you to provide the information at the earliest as per the provisions of the Act.

Thank you.

Date: {{ date }}  
Place: {{ applicant_address }}  

Sincerely,  
{{ applicant_name }}
"""

def generate_rti(user_data):
    template = Template(rti_template)
    return template.render(user_data)

def show_rti_page():
    st.title("📄 RTI Application Generator")

    # Step 1: Collect user inputs
    applicant_name = st.text_input("Enter your full name")
    applicant_address = st.text_area("Enter your address")
    public_authority = st.text_input("Enter the Public Authority (department/office)")
    subject = st.text_input("Enter the subject of information requested")
    information_details = st.text_area("Describe the information you are requesting")
    date = st.date_input("Enter date of application")

    # Step 2: Generate RTI
    if st.button("Generate RTI Application"):
        user_data = {
            "applicant_name": applicant_name,
            "applicant_address": applicant_address,
            "public_authority": public_authority,
            "subject": subject,
            "information_details": information_details,
            "date": date.strftime("%d %B %Y")
        }

        rti_text = generate_rti(user_data)
        st.subheader("Generated RTI Application")
        st.text_area("RTI Application", rti_text, height=400)

        # Convert to PDF with bold headings & key fields
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Bold headings and user-specific info
        headings = ["TO", "Subject", "Dear Sir/Madam,", "Thank you.", "Sincerely,"]
        bold_words = [applicant_name, applicant_address, public_authority, subject]

        for line in rti_text.split("\n"):
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
            label="Download RTI as PDF",
            data=open(temp_file.name, "rb").read(),
            file_name="RTI_Application.pdf",
            mime="application/pdf"
        )
