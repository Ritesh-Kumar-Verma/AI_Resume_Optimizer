
import streamlit as st

st.title("AI Resume Optimizer")

col1 , col2 = st.columns(2)

with col1:
    jd = st.text_area("Enter job description",placeholder="Here...",height=300)






with col2:
    file = st.file_uploader("Upload Resume")
    
    resume_text = st.text_area("Enter Resume Text",height=185,placeholder="Here...")





if st.button("Optimize"):
    st.write(f"Button Pressed{jd},{resume_text}")


st.markdown("---")






