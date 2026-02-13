# pages/admin.py
import streamlit as st
import pandas as pd
from database.db import get_connection
import time

def fetch_all_lawyers():
    """Fetches all lawyers from the database."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM lawyers", conn)
    conn.close()
    return df

def show_admin_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>🛠️ Admin Panel</h1>", unsafe_allow_html=True)
    st.divider()

    # --- 1. VIEW ALL LAWYERS ---
    st.subheader("📋 Registered Lawyers Registry")
    lawyers_df = fetch_all_lawyers()
    
    if lawyers_df.empty:
        st.info("No lawyers found in the database.")
    else:
        st.dataframe(lawyers_df, use_container_width=True, hide_index=True)

    st.divider()

    # --- 2. MANAGE LAWYERS (UPDATE / DELETE) ---
    st.subheader("✏️ Manage Profiles")

    # Create the list of options
    lawyer_options = ["-- Select a lawyer to manage --"] + lawyers_df["name"].tolist()

    selected_lawyer_name = st.selectbox(
        "Select a Lawyer:", 
        options=lawyer_options,
        index=0,
        key="lawyer_select"
    )

    if selected_lawyer_name != "-- Select a lawyer to manage --":
        
        # Get the row for the selected lawyer
        lawyer_data = lawyers_df[lawyers_df["name"] == selected_lawyer_name].iloc[0]
        lawyer_id = int(lawyer_data["id"])

        # --- PREPARE SPECIALIZATION DROPDOWN ---
        # Standard list of specializations
        specialization_options = [
            "Civil Lawyer", "Criminal Lawyer", "Family Lawyer", "Corporate Lawyer",
                "Tax Lawyer", "Cyber Lawyer", "Property Lawyer", "Immigration Lawyer",
                "Labour & Employment Lawyer", "Consumer Protection Lawyer", "Intellectual Property Lawyer"
        ]
        
        # Get current specialization
        current_spec = lawyer_data["specialization"]
        
        # If the current specialization is not in our standard list, add it temporarily
        # so the dropdown works correctly without error.
        if current_spec not in specialization_options:
            specialization_options.insert(0, current_spec)
        
        # Find the index of the current specialization to set as default
        default_spec_index = specialization_options.index(current_spec)

        form_container = st.container(border=True)

        with form_container:
            st.markdown(f"### 📝 Editing: **{lawyer_data['name']}**")
            
            with st.form("update_lawyer_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Full Name", value=lawyer_data["name"])
                    
                    # --- CHANGED TO DROPDOWN ---
                    new_spec = st.selectbox(
                        "Specialization", 
                        options=specialization_options, 
                        index=default_spec_index
                    )
                    
                    new_exp = st.number_input("Experience (Years)", value=int(lawyer_data["experience"]), min_value=0)
                with col2:
                    new_fees = st.number_input("Consultation Fees (₹)", value=float(lawyer_data["fees"]), min_value=0.0)
                    new_loc = st.text_input("Location", value=lawyer_data["location"])
                    new_contact = st.text_input("Contact Number", value=lawyer_data["contact"])

                # Buttons
                submit_col, delete_col = st.columns([1, 1])
                
                with submit_col:
                    update_submitted = st.form_submit_button("Update Profile", type="primary", use_container_width=True)
                
                with delete_col:
                    delete_submitted = st.form_submit_button("Delete Profile", type="secondary", use_container_width=True)

                if update_submitted:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE lawyers 
                        SET name=?, specialization=?, experience=?, fees=?, location=?, contact=?
                        WHERE id=?
                    """, (new_name, new_spec, new_exp, new_fees, new_loc, new_contact, lawyer_id))
                    conn.commit()
                    conn.close()

                    st.success(f"✅ Successfully updated profile for **{new_name}**!")
                    time.sleep(3)
                    
                    # Delete key to reset form
                    if "lawyer_select" in st.session_state:
                        del st.session_state["lawyer_select"]
                    
                    st.rerun()

                if delete_submitted:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM lawyers WHERE id=?", (lawyer_id,))
                    conn.commit()
                    conn.close()

                    st.warning(f"🗑️ Profile for **{lawyer_data['name']}** has been deleted.")
                    time.sleep(3)
                    
                    if "lawyer_select" in st.session_state:
                        del st.session_state["lawyer_select"]
                        
                    st.rerun()