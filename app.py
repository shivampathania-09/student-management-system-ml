import streamlit as st
import pandas as pd
import os
from src.data_handler import StudentManager

# Configure page settings
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #1f2937;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1.2rem;
        color: #4b5563;
    }
    h1, h2, h3 {
        color: #1f2937;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Student Management Dashboard")
st.markdown("Welcome to the Student Management System. Use the sidebar to navigate between records, analytics, and grade prediction.")

# Load data for KPIs
manager = StudentManager()
try:
    df = manager.view_students()
except Exception:
    df = pd.DataFrame()

if not df.empty:
    st.subheader("Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Avg Attendance", f"{df['attendance_percentage'].mean():.1f}%")
    with col3:
        st.metric("Avg Participation", f"{df['class_participation'].mean():.1f}/10")
    with col4:
        st.metric("Avg Score", f"{df['total_score'].mean():.1f}")
        
    st.markdown("---")
    st.subheader("Recent Activity")
    st.dataframe(df.tail(5), use_container_width=True)
else:
    st.info("No student records found. Head to the 'Student Records' page to add data.")
