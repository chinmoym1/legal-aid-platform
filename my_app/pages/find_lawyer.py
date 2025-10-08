# pages/find_lawyer.py
import streamlit as st
from database.db import get_connection, init_db
import pandas as pd

def show_find_lawyer():
    init_db()

    st.markdown("<h1 style='text-align: center; color: #004AAD;'>🔍 Find a Lawyer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Use the filters in the sidebar to find a legal professional that matches your needs.</p>", unsafe_allow_html=True)
    st.divider()

    # --- Sidebar for Search Filters ---
    with st.sidebar:
        st.header(" refined Your Search")
        
        # We use a form to prevent the app from re-running on every filter change
        with st.form("filter_form"):
            specializations = [
                "Any", "Civil Lawyer", "Criminal Lawyer", "Family Lawyer", "Corporate Lawyer",
                "Tax Lawyer", "Cyber Lawyer", "Property Lawyer", "Immigration Lawyer",
                "Labour & Employment Lawyer", "Consumer Protection Lawyer", "Intellectual Property Lawyer"
            ]
            specialization = st.selectbox("Specialization", specializations)
            location = st.text_input("City or State")
            min_experience = st.slider("Minimum Experience (years)", 0, 30, 0)
            min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, step=0.5)
            
            sort_by = st.selectbox(
                "Sort results by",
                ["Rating (High to Low)", "Experience (High to Low)", "Fees (Low to High)"]
            )

            # The search button is the only thing that triggers a re-run
            submitted = st.form_submit_button("🔍 Search Lawyers", type="primary")

    # --- Database Query (only runs when the form is submitted) ---
    if submitted:
        conn = get_connection()
        query = "SELECT * FROM lawyers WHERE 1=1"
        params = []

        if specialization and specialization != "Any":
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

        # Sorting logic
        if "Rating" in sort_by:
            query += " ORDER BY rating DESC"
        elif "Experience" in sort_by:
            query += " ORDER BY experience DESC"
        elif "Fees" in sort_by:
            query += " ORDER BY fees ASC"

        df = pd.read_sql(query, conn, params=params)
        conn.close()
        
        # Store results in session state to persist them
        st.session_state.search_results = df

    # --- Display Results in the Main Page Area ---
    if 'search_results' in st.session_state:
        df = st.session_state.search_results
        
        if df.empty:
            st.warning("⚠️ No matching lawyers found. Try broadening your search filters in the sidebar.")
        else:
            st.success(f"✅ Found {len(df)} lawyer(s) matching your criteria.")
            st.write("") # Spacer

            # Display each lawyer as a card
            for _, row in df.iterrows():
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {row['name']}")
                        st.markdown(f"**{row['specialization']}**")
                        st.write(f"📍 {row['location']}")
                        st.write(f"💼 **{row['experience']}** years of experience")
                        st.write(f"📞 Contact: **{row['contact']}**")
                    with col2:
                        st.markdown(f"<h3 style='text-align: right; color: #004AAD;'>⭐ {row['rating']:.1f} / 5.0</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='text-align: right;'>Avg. Fees: <b>₹{row['fees']:,}</b></p>", unsafe_allow_html=True)

    else:
        # Initial state before any search is performed
        st.info("Please use the filters on the left and click 'Search' to see results.")