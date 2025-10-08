# pages/register_lawyer.py
import streamlit as st
from database.db import get_connection, init_db

def calculate_rating(experience: int) -> float:
    """Auto-assign rating based on experience years."""
    if experience < 1: return 2.5
    elif experience < 3: return 3.0
    elif experience < 5: return 3.5
    elif experience < 10: return 4.0
    elif experience < 20: return 4.5
    else: return 5.0

def show_register_lawyer():
    init_db()

    st.markdown("<h1 style='text-align: center; color: #004AAD;'>👨‍⚖️ Register as a Lawyer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Join our network of legal professionals. Fill out the form below to be listed in our directory.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Create a more visually appealing form layout ---
    # We'll center the form and give it a max width to look better on wide screens
    _, col2, _ = st.columns([1, 1.5, 1])

    with col2:
        with st.container(border=True):
            with st.form("register_form", clear_on_submit=True):
                st.subheader("Your Professional Details")

                # Using columns for a more compact form
                c1, c2 = st.columns(2)
                with c1:
                    name = st.text_input("Full Name", key="reg_name")
                    experience = st.number_input("Experience (in years)", min_value=0, step=1, key="reg_exp")
                    location = st.text_input("Primary Location (City, State)", key="reg_loc")
                with c2:
                    specializations = [
                        "Civil Lawyer", "Criminal Lawyer", "Family Lawyer", "Corporate Lawyer",
                        "Tax Lawyer", "Cyber Lawyer", "Property Lawyer", "Immigration Lawyer",
                        "Labour & Employment Lawyer", "Consumer Protection Lawyer", "Intellectual Property Lawyer"
                    ]
                    specialization = st.selectbox("Area of Specialization", specializations, key="reg_spec")
                    fees = st.number_input("Fees (per consultation, in ₹)", min_value=0.0, step=100.0, key="reg_fees")
                    contact = st.text_input("Contact (Phone or Email)", key="reg_contact")

                submitted = st.form_submit_button("Register Profile", use_container_width=True, type="primary")

    # --- Form Submission Logic (unchanged, but moved outside the columns) ---
    if submitted:
        # Simple validation
        if not all([name, specialization, location, contact]):
            st.warning("Please fill out all fields.")
        else:
            rating = calculate_rating(experience)

            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO lawyers (name, specialization, experience, rating, fees, location, contact) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (name, specialization, experience, rating, fees, location, contact)
                )
                conn.commit()
                conn.close()
                st.success(f"✅ Thank you for registering, {name}! Your profile has been created with a system-assigned rating of ⭐ {rating:.1f}.")
            except Exception as e:
                st.error(f"An error occurred while registering: {e}")