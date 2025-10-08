# pages/dispute.py
import streamlit as st
from jinja2 import Template
from fpdf import FPDF
import tempfile
import datetime

# --- 1. TEMPLATE AND GENERATION LOGIC (Unchanged) ---
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
Place: {{ complainant_place }}

Sincerely,
{{ complainant_name }}
"""

def generate_dispute(user_data):
    template = Template(dispute_template)
    return template.render(user_data)


# --- 2. REDESIGNED STREAMLIT UI FUNCTION ---
def show_dispute_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>📄 Customer Complaint Letter Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Fill in the details below to generate a formal complaint letter for a product or service.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Two-Column Layout for the entire page ---
    col1, col2 = st.columns([1.2, 1])

    # --- COLUMN 1: DATA INPUT FORM ---
    with col1:
        st.subheader("1. Enter Complaint Details")

        with st.container(border=True):
            st.markdown("##### Your Information")
            complainant_name = st.text_input("Enter your full name", key="disp_name")
            complainant_address = st.text_area("Enter your full address", height=100, key="disp_address")

            st.markdown("##### Company Information")
            company_name = st.text_input("Enter the company/organization name", key="disp_comp_name")
            company_address = st.text_area("Enter the company address", height=100, key="disp_comp_address")
            
            st.markdown("##### Dispute Details")
            product_service = st.text_input("Product or Service in dispute", key="disp_product")
            issue_details = st.text_area("Describe the issue in detail", height=150, help="Provide dates, order numbers, and a clear description of the problem.", key="disp_issue")
            desired_resolution = st.text_area("What is your desired resolution?", height=100, help="e.g., a full refund, a replacement product, a formal apology.", key="disp_resolution")
            date_val = st.date_input("Enter date of complaint", datetime.date.today(), key="disp_date")

        # The generate button is the primary action for the form
        if st.button("✨ Generate Complaint Letter", use_container_width=True, type="primary"):
            if not all([complainant_name, complainant_address, company_name, product_service, issue_details]):
                st.warning("Please fill in all required fields before generating.")
            else:
                date_str = date_val.strftime("%d %B %Y")
                complainant_place = complainant_address.split('\n')[-1] if complainant_address else ""
                user_data = {
                    "complainant_name": complainant_name, "complainant_address": complainant_address,
                    "company_name": company_name, "company_address": company_address,
                    "product_service": product_service, "issue_details": issue_details,
                    "desired_resolution": desired_resolution, "date": date_str,
                    "complainant_place": complainant_place
                }
                # Store data in session state for the second column
                st.session_state['dispute_text'] = generate_dispute(user_data)
                st.session_state['dispute_user_data'] = user_data
                st.rerun()

    # --- COLUMN 2: PREVIEW AND DOWNLOAD ---
    with col2:
        st.subheader("2. Preview and Download")

        if 'dispute_text' in st.session_state:
            dispute_text = st.session_state['dispute_text']
            user_data = st.session_state['dispute_user_data']

            # Display the preview
            st.text_area("Letter Preview", dispute_text, height=700)

            # --- ORIGINAL PDF GENERATION CODE (UNCHANGED, AS REQUESTED) ---
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            line_height = 6

            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, "TO\n")
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, "The Manager / Customer Service Officer\n")
            pdf.write(line_height, f"{user_data['company_name']}\n")
            pdf.write(line_height, f"{user_data['company_address']}\n\n")

            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, f"Subject: Complaint / Dispute Regarding {user_data['product_service']}\n\n")

            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, "Dear Sir/Madam,\n\n")

            pdf.write(line_height, f"I, {user_data['complainant_name']}, residing at {user_data['complainant_address']}, am writing to formally lodge a complaint regarding {user_data['product_service']}.\n\n")

            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, "Details of the issue:\n")
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, f"{user_data['issue_details']}\n\n")

            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, "I request the following resolution:\n")
            pdf.set_font("Arial", "", 12)
            pdf.write(line_height, f"{user_data['desired_resolution']}\n\n")

            pdf.write(line_height, "I hope this matter will be resolved promptly as per your company policies and applicable laws.\n\n")
            pdf.write(line_height, "Thank you.\n\n")

            pdf.write(line_height, f"Date: {user_data['date']}\n")
            pdf.write(line_height, f"Place: {user_data['complainant_place']}\n\n")

            pdf.write(line_height, "Sincerely,\n\n\n\n")
            pdf.set_font("Arial", "B", 12)
            pdf.write(line_height, user_data['complainant_name'])
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                pdf_file_path = tmp.name
                pdf.output(pdf_file_path)
            with open(pdf_file_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="⬇️ Download Complaint as PDF",
                data=pdf_bytes,
                file_name="Customer_Dispute.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            # Placeholder for the right column
            with st.container(border=True, height=700):
                st.info("Your complaint letter preview and download button will appear here after you fill out the form and click 'Generate'.")