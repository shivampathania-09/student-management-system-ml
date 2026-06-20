import streamlit as st
from src.data_handler import StudentManager

st.set_page_config(page_title="Student Records", page_icon="📋", layout="wide")
st.title("📋 Student Records Management")

manager = StudentManager()

tab1, tab2, tab3, tab4 = st.tabs(["View All", "Add Student", "Update Student", "Delete Student"])

with tab1:
    st.subheader("All Student Records")
    
    # Sidebar filters
    with st.sidebar:
        st.header("Search & Filter")
        search_query = st.text_input("Search by Student ID", "")
        st.divider()
        st.header("Pagination")
        records_per_page = st.selectbox("Records per page", [50, 100, 200, 500])
    
    # Pagination state
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 1
        
    if 'prev_search' not in st.session_state:
        st.session_state.prev_search = search_query

    # Reset page if search query changes
    if search_query != st.session_state.prev_search:
        st.session_state.page_number = 1
        st.session_state.prev_search = search_query
    offset = (st.session_state.page_number - 1) * records_per_page
    
    df, total_count = manager.get_students_paginated(limit=records_per_page, offset=offset, search_query=search_query)
    
    total_pages = (total_count + records_per_page - 1) // records_per_page
    if total_pages == 0:
        total_pages = 1

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        
        # Pagination controls
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("Previous") and st.session_state.page_number > 1:
                st.session_state.page_number -= 1
                st.rerun()
        with col2:
            st.write(f"Page {st.session_state.page_number} of {total_pages} (Total Records: {total_count})")
        with col3:
            if st.button("Next") and st.session_state.page_number < total_pages:
                st.session_state.page_number += 1
                st.rerun()
    else:
        st.info("No records to display.")

with tab2:
    st.subheader("Add New Student")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID")
            attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, step=1.0)
            participation = st.number_input("Participation (0-10)", min_value=0.0, max_value=10.0, step=0.1)
        with col2:
            total_score = st.number_input("Total Score", min_value=0.0, max_value=100.0, step=1.0)
            grade = st.text_input("Current Grade (Optional)")
            
        submitted = st.form_submit_button("Add Student", type="primary")
        if submitted:
            if student_id:
                try:
                    manager.add_student(student_id, attendance, participation, total_score, grade)
                    st.success(f"Student {student_id} added successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("Student ID is required.")

with tab3:
    st.subheader("Update Student Record")
    update_id = st.text_input("Enter Student ID to update")
    if update_id:
        student = manager.search_student(update_id)
        if student:
            with st.form("update_form"):
                st.write(f"Updating records for **{update_id}**")
                u_att = st.number_input("Attendance (%)", value=float(student['attendance_percentage']))
                u_part = st.number_input("Participation", value=float(student['class_participation']))
                u_score = st.number_input("Total Score", value=float(student['total_score']))
                u_grade = st.text_input("Grade", value=str(student['grade']))
                
                if st.form_submit_button("Save Changes"):
                    try:
                        manager.update_student(update_id, 
                                               attendance_percentage=u_att,
                                               class_participation=u_part,
                                               total_score=u_score,
                                               grade=u_grade)
                        st.success("Record updated!")
                    except Exception as e:
                        st.error(f"Update failed: {e}")
        else:
            st.warning("Student ID not found.")

with tab4:
    st.subheader("Delete Student")
    del_id = st.text_input("Enter Student ID to delete")
    if st.button("Delete Record", type="primary"):
        if del_id:
            try:
                manager.delete_student(del_id)
                st.success(f"Student {del_id} deleted.")
            except KeyError:
                st.error("Student ID not found.")
