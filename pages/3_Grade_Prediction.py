import streamlit as st
from src.model_pipeline import predict_grade
from src.data_handler import StudentManager

st.set_page_config(page_title="Grade Prediction", page_icon="🤖", layout="wide")
st.title("🤖 ML Grade Prediction")
st.markdown("Enter student metrics to predict their final grade using the trained Random Forest model.")

manager = StudentManager()

with st.container():
    st.subheader("Predict from Existing Student")
    student_id = st.text_input("Enter Student ID to auto-fill data")
    
    if student_id:
        student = manager.search_student(student_id)
        if student:
            st.success(f"Loaded data for {student_id}")
            att = float(student['attendance_percentage'])
            part = float(student['class_participation'])
            score = float(student['total_score'])
        else:
            st.warning("Student not found.")
            att, part, score = 0.0, 0.0, 0.0
    else:
        att, part, score = 0.0, 0.0, 0.0

st.markdown("---")

with st.form("predict_form"):
    st.subheader("Model Inputs")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        attendance = st.number_input("Attendance (%)", value=att, min_value=0.0, max_value=100.0)
    with col2:
        participation = st.number_input("Participation (0-10)", value=part, min_value=0.0, max_value=10.0)
    with col3:
        total_score = st.number_input("Total Score", value=score, min_value=0.0, max_value=100.0)
        
    submitted = st.form_submit_button("Predict Grade", type="primary")
    
    if submitted:
        with st.spinner("Analyzing data..."):
            result = predict_grade(attendance, participation, total_score)
            
        if result and result[0] is not None:
            grade, confidence = result
            
            st.success("Prediction Complete!")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Predicted Grade", grade)
            with col_res2:
                if confidence:
                    st.metric("Model Confidence", f"{confidence}%")
                    
            if student_id:
                manager.update_student(student_id, grade=grade)
                st.info(f"Automatically saved predicted grade '{grade}' to Student {student_id}'s record.")
        else:
            st.error(f"Error: {result[1]}")
