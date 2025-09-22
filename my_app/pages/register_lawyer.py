import streamlit as st
from database.db import get_connection, init_db

def calculate_rating(experience: int) -> float:
    """Auto-assign rating based on experience years."""
    if experience < 1:
        return 2.5
    elif experience < 3:
        return 3.0
    elif experience < 5:
        return 3.5
    elif experience < 10:
        return 4.0
    elif experience < 20:
        return 4.5
    else:
        return 5.0

def show_register_lawyer():
    init_db()
    st.title("👨‍⚖️ Register as a Lawyer")

    specializations = [
        "Civil Lawyer",
        "Criminal Lawyer",
        "Family Lawyer",
        "Corporate Lawyer",
        "Constitutional Lawyer",
        "Tax Lawyer",
        "Intellectual Property (IP) Lawyer",
        "Labour & Employment Lawyer",
        "Consumer Protection Lawyer",
        "Cyber Lawyer",
        "Property / Real Estate Lawyer",
        "Immigration Lawyer",
        "Environmental Lawyer",
        "Human Rights Lawyer",
        "Medical / Health Lawyer",
        "Banking & Finance Lawyer",
        "Insurance Lawyer",
        "Education Lawyer",
        "Public Interest Lawyer (PIL)",
        "International Law Lawyer"
    ]

    with st.form("register_form"):
        name = st.text_input("Full Name")
        specialization = st.selectbox("Specialization", specializations)
        experience = st.number_input("Experience (years)", min_value=0, step=1)
        fees = st.number_input("Fees (per consultation)", min_value=0.0, step=100.0)
        location = st.text_input("Location")
        contact = st.text_input("Contact")

        submitted = st.form_submit_button("Register")

        if submitted:
            rating = calculate_rating(experience)  # ✅ auto-calculated

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO lawyers 
                (name, specialization, experience, rating, fees, location, contact) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, specialization, experience, rating, fees, location, contact)
            )
            conn.commit()
            conn.close()
            st.success(f"✅ Lawyer registered successfully! (System-assigned rating: ⭐ {rating})")
