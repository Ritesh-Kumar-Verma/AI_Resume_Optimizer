
import streamlit as st
import json
from streamlit_local_storage import LocalStorage

local_storage = LocalStorage()


st.set_page_config(layout='wide')

st.title("AI Resume Optimizer")



def save_data():
    data = json.dumps(st.session_state.d)
    
    local_storage.setItem(
        "resume_data",
        data
    )


def user_info():
    st.subheader("Enter your Details")
    
    if "d" not in st.session_state:
        st.session_state.d = {}

    if "projects" not in st.session_state:
        st.session_state.projects = []
        
        

    
    basic_left_col , basic_right_col = st.columns(2)
    
    #####Basic Info#####
    basic_info = dict()
    
    with basic_left_col:
        basic_info['name'] = st.text_input("Enter your name")
        basic_info['phone_number'] = st.text_input("Enter your phone number")
        basic_info['email'] = st.text_input("Enter your email")
        basic_info['address'] = st.text_area("Enter your address")
    with basic_right_col:
        basic_info['profile_link'] = st.text_input("Enter your profile/portfolio link")
        basic_info['linkedin'] = st.text_input("Enter your linked url")
        basic_info['github'] = st.text_input("Enter your github url")
    basic_info['summary'] = st.text_area("Enter you summary")
    
    st.write(basic_info)
    
    st.markdown('---')
    
    st.session_state.d['basic_info'] = basic_info
    #####Technical Skills#####

    
    st.subheader("Technical skills")
    technical_left_col, technical_right_col = st.columns(2)
    
    technical_skill = dict()
    
    with technical_left_col:
        
        technical_skill['programming_language'] = st.text_input("Programming language")
        
        technical_skill['frontend'] = st.text_input("Frontend skills")
        
        technical_skill['backend'] = st.text_input("Backend skills")
        
    with technical_right_col:
        technical_skill['database'] = st.text_input("Database knowledge")
        
        technical_skill['ai_ml_data_science'] = st.text_input("AI Info")
        
        
        technical_skill['tools'] = st.text_input("Tools like Vsc, IntelliJ")
        
    
        
    st.session_state.d['technical_skill'] = technical_skill
    
    
    
    st.markdown('---')

    #####Education Info#####
    st.subheader("Education Details")
    
    education = dict()
    
    education_left_col , education_right_col = st.columns(2)

    with education_left_col:
        education['institute_name'] = st.text_input("Enter institute name")
        education['degree_certificate_name'] = st.text_input("Enter Degree/Certificate Name")
    with education_right_col:
        education['location'] = st.text_input("Enter Address of Institute")
        education['duration'] = st.text_input("Enter duration in format 2019-2023")

    st.session_state.d['education'] = education
    st.markdown('---')
    
    
    #####Project Info#####

    
    st.subheader("Project Details")
    project_details()
    
    st.session_state.d['projects'] = st.session_state.projects
    
    if st.button("Create Resume"):
        st.write(st.session_state.d)
        save_data()
    

def project_details():
    with st.form("project_form",clear_on_submit=True):
        title = st.text_input("Project Title")
        tech = st.text_input("Technologies Used")
        year = st.text_input("Project Year")
        frontend = st.text_input("Frontend Code URL")
        backend = st.text_input("Backend Code URL")
        live = st.text_input("Live Demo URL")
        description = st.text_area("Enter your description",placeholder="Enter points seprated with comma")

        submitted = st.form_submit_button("Add Project")

        if submitted:
            st.session_state.projects.append({
                "title": title,
                "tech_used": tech,
                "project_year": year,
                "frontend_code_url": frontend,
                "backend_code_url": backend,
                "live_link": live,
                "description" : description
            })
            st.success("Project added Successfully")
    
    
    



if __name__ == '__main__':
    
    data = local_storage.getItem("resume_data")
    if not data:
        user_info()
        
    st.write("Resume Data Available")