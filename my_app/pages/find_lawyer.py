import streamlit as st
from database.db import get_connection, init_db
import pandas as pd

def show_find_lawyer():
    init_db()

    st.title("🔍 Find a Lawyer")

    # --- Filter Options ---
    specializations = [
        "", "Civil Lawyer", "Criminal Lawyer", "Family Lawyer", "Corporate Lawyer",
        "Tax Lawyer", "Cyber Lawyer", "Property Lawyer", "Immigration Lawyer",
        "Labour & Employment Lawyer", "Consumer Protection Lawyer", "Intellectual Property Lawyer"
    ]

    # --- Search Filters ---
    col1, col2, col3 = st.columns(3)

    with col1:
        specialization = st.selectbox("Specialization", specializations)

    with col2:
        location = st.text_input("Location")

    with col3:
        min_experience = st.slider("Min Experience (yrs)", 0, 30, 0)

    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0)
    max_fees = st.number_input("Maximum Fees", min_value=0.0, step=100.0)

    sort_by = st.selectbox(
        "Sort results by",
        ["Rating (High → Low)", "Fees (Low → High)", "Experience (High → Low)"]
    )

    # --- Fetch Data ---
    conn = get_connection()
    query = "SELECT * FROM lawyers WHERE 1=1"
    params = []

    if specialization:
        query += " AND specialization = ?"
        params.append(specialization)

    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")

    if min_experience > 0:
        query += " AND experience >= ?"
        params.append(min_experience)

    if min_rating > 0:
        query += " AND rating >= ?"
        params.append(min_rating)

    if max_fees > 0:
        query += " AND fees <= ?"
        params.append(max_fees)

    # Sorting
    if "Rating" in sort_by:
        query += " ORDER BY rating DESC"
    elif "Fees" in sort_by:
        query += " ORDER BY fees ASC"
    elif "Experience" in sort_by:
        query += " ORDER BY experience DESC"

    df = pd.read_sql(query, conn, params=params)
    conn.close()

    # --- Display Results ---
    if df.empty:
        st.warning("⚠️ No matching lawyers found. Try adjusting filters.")
    else:
        st.success(f"✅ Found {len(df)} lawyer(s)")

        for _, row in df.iterrows():
            with st.expander(f"👨‍⚖️ {row['name']} - {row['specialization']}"):
                st.write(f"📍 Location: {row['location']}")
                st.write(f"💼 Experience: {row['experience']} years")
                st.write(f"⭐ Rating: {row['rating']}")
                st.write(f"💰 Fees: ₹{row['fees']}")
                st.write(f"📞 Contact: {row['contact']}")

