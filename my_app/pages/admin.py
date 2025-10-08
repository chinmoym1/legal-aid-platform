# pages/admin.py
import streamlit as st
import pandas as pd
from database.db import get_connection

def fetch_all_lawyers():
    """Fetches all lawyers from the database and returns a DataFrame."""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM lawyers", conn)
    conn.close()
    return df

def show_admin_page():
    st.markdown("<h1 style='text-align: center; color: #004AAD;'>🛠️ Admin Panel: Manage Lawyers</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Here you can view, update, and delete lawyer profiles from the database.</p>", unsafe_allow_html=True)
    st.divider()

    # --- 1. Display All Lawyers in a Table ---
    st.subheader("All Registered Lawyers")
    try:
        lawyers_df = fetch_all_lawyers()
        if lawyers_df.empty:
            st.info("No lawyers are currently registered in the database.")
        else:
            st.dataframe(lawyers_df, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to load lawyer data: {e}")
        return # Stop execution if data can't be loaded

    st.divider()

    # --- 2. Select a Lawyer to Edit or Delete ---
    st.subheader("Update or Delete a Lawyer Profile")

    # Use the names from the DataFrame to populate the selectbox
    lawyer_list = ["-- Select a lawyer to manage --"] + lawyers_df["name"].tolist()
    selected_lawyer_name = st.selectbox("Choose a lawyer:", lawyer_list)

    if selected_lawyer_name != "-- Select a lawyer to manage --":
        # Get the full details of the selected lawyer
        lawyer_data = lawyers_df[lawyers_df["name"] == selected_lawyer_name].iloc[0]

        # --- UPDATE FORM ---
        with st.container(border=True):
            st.markdown(f"#### ✏️ Editing Profile for: {lawyer_data['name']}")
            with st.form("update_form"):
                # Populate the form with the lawyer's current data
                new_name = st.text_input("Full Name", value=lawyer_data["name"])
                new_spec = st.text_input("Specialization", value=lawyer_data["specialization"])
                new_exp = st.number_input("Experience (years)", value=int(lawyer_data["experience"]))
                new_fees = st.number_input("Fees", value=float(lawyer_data["fees"]))
                new_loc = st.text_input("Location", value=lawyer_data["location"])
                new_contact = st.text_input("Contact", value=lawyer_data["contact"])
                
                update_button = st.form_submit_button("Update Profile", use_container_width=True, type="primary")

                if update_button:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE lawyers 
                        SET name=?, specialization=?, experience=?, fees=?, location=?, contact=?
                        WHERE id=?
                        """,
                        (new_name, new_spec, new_exp, new_fees, new_loc, new_contact, int(lawyer_data["id"]))
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"✅ Profile for {new_name} has been updated successfully!")
                    st.rerun() # Rerun to refresh the table above

        st.write("") # Spacer

        # --- DELETE SECTION ---
        with st.container(border=True):
            st.markdown(f"#### 🗑️ Delete Profile for: {lawyer_data['name']}")
            st.warning("This action is permanent and cannot be undone.", icon="⚠️")
            
            if st.button(f"Permanently Delete {lawyer_data['name']}'s Profile", use_container_width=True):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM lawyers WHERE id=?", (int(lawyer_data["id"]),))
                conn.commit()
                conn.close()
                st.success(f"Profile for {lawyer_data['name']} has been deleted.")
                # Clear the selection and rerun to update the page
                st.session_state.clear()
                st.rerun()