# pages/rti.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile
import datetime

# --- 1. TEMPLATE AND GENERATION LOGIC (Unchanged) ---
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
Place: {{ applicant_place }}

Sincerely,
{{ applicant_name }}
"""

def generate_rti(user_data):
    template = Template(rti_template)
    return template.render(user_data)


# --- 2. REDESIGNED STREAMLIT UI FUNCTION ---
def show_rti_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>📄 RTI Application Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Fill in the details to generate a formal Right to Information (RTI) application, ready for submission.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Two-Column Layout for the entire page ---
    col1, col2 = st.columns([1.2, 1])

    # --- COLUMN 1: DATA INPUT FORM ---
    with col1:
        st.subheader("1. Enter Application Details")
        
        with st.container(border=True):
            applicant_name = st.text_input("Enter your full name", key="rti_name")
            applicant_address = st.text_area("Enter your full address", height=100, key="rti_address")
            public_authority = st.text_input("Enter the Public Authority (department/office)", key="rti_authority")
            subject = st.text_input("Enter the subject of information requested", key="rti_subject")
            information_details = st.text_area("Describe the specific information you are requesting", height=150, help="Be specific. Use numbered points for multiple queries.", key="rti_details")
            date_val = st.date_input("Enter date of application", datetime.date.today(), key="rti_date")

        # The generate button is the primary action for the form
        if st.button("✨ Generate RTI Application", use_container_width=True, type="primary"):
            if not all([applicant_name, applicant_address, public_authority, subject, information_details]):
                st.warning("Please fill in all required fields before generating.")
            else:
                date_str = date_val.strftime("%d %B %Y")
                applicant_place = applicant_address.split('\n')[-1] if applicant_address else ""
                user_data = {
                    "applicant_name": applicant_name,
                    "applicant_address": applicant_address,
                    "public_authority": public_authority,
                    "subject": subject,
                    "information_details": information_details,
                    "date": date_str,
                    "applicant_place": applicant_place
                }
                # Store data in session state for the second column to use
                st.session_state['rti_text'] = generate_rti(user_data)
                st.session_state['rti_user_data'] = user_data
                st.rerun() # Rerun to make the output appear immediately

    # --- COLUMN 2: PREVIEW AND DOWNLOAD ---
    with col2:
        st.subheader("2. Preview and Download")

        if 'rti_text' in st.session_state:
            rti_text = st.session_state['rti_text']
            user_data = st.session_state['rti_user_data']

            # Display the preview
            st.text_area("Application Preview", rti_text, height=600)

            # --- ORIGINAL PDF GENERATION CODE (UNCHANGED, AS REQUESTED) ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            line_height = 6

            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, "TO\n")
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, "The Public Information Officer\n")
            pdf.write(line_height, f"{user_data['public_authority']}\n\n")
            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, "Subject: Request for information under the RTI Act, 2005\n\n")
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, "Dear Sir/Madam,\n\n")
            pdf.write(line_height, f"I, {user_data['applicant_name']}, residing at {user_data['applicant_address']}, hereby request the following information under the Right to Information Act, 2005:\n\n")
            pdf.set_font("Arial", "I", 12)
            pdf.multi_cell(0, line_height, user_data['information_details'])
            pdf.ln(3)
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, f"The subject of this request is: {user_data['subject']}.\n\n")
            pdf.write(line_height, "I am enclosing the required application fee (if applicable) and request you to provide the information at the earliest as per the provisions of the Act.\n\n")
            pdf.write(line_height, "Thank you.\n\n")
            pdf.write(line_height, f"Date: {user_data['date']}\n")
            pdf.write(line_height, f"Place: {user_data['applicant_place']}\n\n")
            pdf.write(line_height, "Sincerely,\n")
            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, user_data['applicant_name'])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdf_file_path = tmp.name
                pdf.output(pdf_file_path)
            with open(pdf_file_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="⬇️ Download RTI as PDF",
                data=pdf_bytes,
                file_name="RTI_Application.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            # Placeholder for the right column before generation
            with st.container(border=True, height=600):
                st.info("Your application preview and download button will appear here once you fill out the form and click 'Generate'.")