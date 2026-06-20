import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.data_handler import StudentManager

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")
st.title("📊 Data Analytics & Visualizations")

manager = StudentManager()
df = manager.view_students()

if df.empty:
    st.warning("No data available for analytics.")
else:
    sns.set_theme(style="whitegrid")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Grade Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x='grade', order=sorted(df['grade'].unique()), ax=ax, palette="viridis")
        st.pyplot(fig)
        
        st.subheader("Attendance Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df['attendance_percentage'], bins=20, kde=True, color='skyblue', ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Total Score Distribution")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df['total_score'], bins=20, kde=True, color='salmon', ax=ax)
        st.pyplot(fig)
        
        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(6, 4))
        numeric_df = df.select_dtypes(include=['float64', 'int64'])
        if not numeric_df.empty:
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
            st.pyplot(fig)
        else:
            st.write("Not enough numeric data for correlation.")
