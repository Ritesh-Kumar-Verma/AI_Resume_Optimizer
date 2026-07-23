
import streamlit as st
from components.User_Info import User_Info
from streamlit_local_storage import LocalStorage


st.set_page_config(layout='wide')

st.title("AI Resume Optimizer")

if __name__ == '__main__':
    
    local_storage = LocalStorage()
    
    user_Info = User_Info()
    
    data = local_storage.getItem("resume_data")
    
    
    user_Info.user_info()
    
   
    

         