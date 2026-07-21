import streamlit as st
from streamlit_local_storage import LocalStorage
import json
class User_Info:
    
    def __init__(self):
        
        self.local_storage = LocalStorage()
        
        if 'd' not in st.session_state:
            data = self.load_data()
            if data:
                st.session_state.d = data
                st.session_state.projects = data['projects']
            else:
                st.session_state.d = {
                    "basic_info": {
                        "name": "",
                        "phone_number": "",
                        "email": "",
                        "address": "",
                        "profile_link": "",
                        "linkedin": "",
                        "github": "",
                        "summary": ""
                    },
                    "technical_skill": {
                        "programming_language": "",
                        "frontend": "",
                        "backend": "",
                        "database": "",
                        "ai_ml_data_science": "",
                        "tools": ""
                    },
                    "education": {
                        "institute_name": "",
                        "degree_certificate_name": "",
                        "location": "",
                        "duration": ""
                    },
                    "projects": []
                    }
                st.session_state.projects = []
                # st.session_state.projects = [{
                #         "title": "",
                #         "tech_used": "",
                #         "project_year": "",
                #         "frontend_code_url": "",
                #         "backend_code_url": "",
                #         "live_link": "",
                #         "description" : ""
                #     }]

        # if "projects" not in st.session_state:
        

    
    def save_data(self):
        data = json.dumps(st.session_state.d)        # d is dictionary
        
        self.local_storage.setItem(
            "resume_data",
            data
        )
    def load_data(self):
        data = self.local_storage.getItem("resume_data")
        if data is None:
            return {}
        data = json.loads(data)
        return data 
        
    def display_details(self):
        st.write(self.load_data())
    
    
    def project_details(self,project,index):
        with st.form(key=f'project_{index}',clear_on_submit=True):
            title = st.text_input("Project Title",value=project['title'])
            tech_used = st.text_input("Technologies Used",value=project['tech_used'])
            project_year = st.text_input("Project Year",value=project['project_year'])
            frontend_code_url = st.text_input("Frontend Code URL",value=project['frontend_code_url'])
            backend_code_url = st.text_input("Backend Code URL",value=project['backend_code_url'])
            live_link = st.text_input("Live Demo URL",value=project['live_link'])
            description = st.text_area("Enter your description",placeholder="Enter points seprated with comma",value=project['description'])
            submitted = st.form_submit_button("Update Project")

            if submitted:
                st.session_state.projects[index] = {
                    "title": title,
                    "tech_used": tech_used,
                    "project_year": project_year,
                    "frontend_code_url": frontend_code_url,
                    "backend_code_url": backend_code_url,
                    "live_link": live_link,
                    "description" : description
                }
                st.session_state.d['projects'] = st.session_state.projects
                st.success("Project updated Successfully")
                
                
                
    def display_projects(self):

        st.subheader("Project Details")

        if len(st.session_state.projects) == 0:
            st.info("No projects added yet")
            return

        if "edit_project" not in st.session_state:
            st.session_state.edit_project = None

        for index, project in enumerate(st.session_state.projects):

            with st.expander(
                f"{index+1}. {project['title'] if project['title'] else 'Untitled Project'}"
            ):

                st.write("### Title")
                st.write(project["title"])
                st.write("### Technologies")
                st.write(project["tech_used"])
                st.write("### Year")
                st.write(project["project_year"])
                st.write("### Frontend Code")
                st.write(project["frontend_code_url"])
                st.write("### Backend Code")
                st.write(project["backend_code_url"])
                st.write("### Live Link")
                st.write(project["live_link"])
                st.write("### Description")
                st.write(project["description"])

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✏ Edit", key=f"edit_{index}"):
                        st.session_state.edit_project = index

                with col2:
                    if st.button("🗑 Delete", key=f"delete_{index}"):

                        st.session_state.projects.pop(index)
                        st.session_state.d["projects"] = st.session_state.projects

                        if st.session_state.edit_project == index:
                            st.session_state.edit_project = None

                        st.rerun()

                if st.session_state.edit_project == index:
                    self.project_details(project, index)   
                
                
    def add_project(self):
        with st.form(key='project_',clear_on_submit=True):
            title = st.text_input("Project Title")
            tech_used = st.text_input("Technologies Used")
            project_year = st.text_input("Project Year")
            frontend_code_url = st.text_input("Frontend Code URL")
            backend_code_url = st.text_input("Backend Code URL")
            live_link = st.text_input("Live Demo URL")
            description = st.text_area("Enter your description",placeholder="Enter points seprated with comma")
            submitted = st.form_submit_button("Add Project")
            if submitted:
                st.session_state.projects.append({
                    "title": title,
                    "tech_used": tech_used,
                    "project_year": project_year,
                    "frontend_code_url": frontend_code_url,
                    "backend_code_url": backend_code_url,
                    "live_link": live_link,
                    "description" : description
                })
                st.session_state.d['projects'] = st.session_state.projects
                st.success("Project added Successfully")
                st.session_state.show_project_form = False
                st.rerun()
                
        
    def user_info(self):
        
        st.subheader("Enter your Details")
        
        basic_left_col , basic_right_col = st.columns(2)
        
        #####Basic Info#####
        basic_info = dict()
        with basic_left_col:
            basic_info['name'] = st.text_input("Enter your name",value=st.session_state.d['basic_info']['name'])
            basic_info['phone_number'] = st.text_input("Enter your phone number",value=st.session_state.d['basic_info']['phone_number'])
            basic_info['email'] = st.text_input("Enter your email",value=st.session_state.d['basic_info']['email'])
            basic_info['address'] = st.text_area("Enter your address",value=st.session_state.d['basic_info']['address'])
        with basic_right_col:
            basic_info['profile_link'] = st.text_input("Enter your profile/portfolio link",value=st.session_state.d['basic_info']['profile_link'])
            basic_info['linkedin'] = st.text_input("Enter your linked url",value=st.session_state.d['basic_info']['linkedin'])
            basic_info['github'] = st.text_input("Enter your github url",value=st.session_state.d['basic_info']['github'])
        basic_info['summary'] = st.text_area("Enter you summary",value=st.session_state.d['basic_info']['summary'])
        
        
        st.markdown('---')
        
        st.session_state.d['basic_info'] = basic_info
        #####Technical Skills#####

        
        st.subheader("Technical skills")
        technical_left_col, technical_right_col = st.columns(2)
        
        technical_skill = dict()
        
        with technical_left_col:
            
            technical_skill['programming_language'] = st.text_input("Programming language",value=st.session_state.d['technical_skill']['programming_language'])
            
            technical_skill['frontend'] = st.text_input("Frontend skills",value=st.session_state.d['technical_skill']['frontend'])
            
            technical_skill['backend'] = st.text_input("Backend skills",value=st.session_state.d['technical_skill']['backend'])
            
        with technical_right_col:
            technical_skill['database'] = st.text_input("Database knowledge",value=st.session_state.d['technical_skill']['database'])
            
            technical_skill['ai_ml_data_science'] = st.text_input("AI Info",value=st.session_state.d['technical_skill']['ai_ml_data_science'])
            
            
            technical_skill['tools'] = st.text_input("Tools like Vsc, IntelliJ",value=st.session_state.d['technical_skill']['tools'])
            
        
            
        st.session_state.d['technical_skill'] = technical_skill
        
        
        
        st.markdown('---')

        #####Education Info#####
        st.subheader("Education Details")
        
        education = dict()
        
        education_left_col , education_right_col = st.columns(2)

        with education_left_col:
            education['institute_name'] = st.text_input("Enter institute name", value=st.session_state.d['education']['institute_name'])
            education['degree_certificate_name'] = st.text_input("Enter Degree/Certificate Name", value=st.session_state.d['education']['degree_certificate_name'])
        with education_right_col:
            education['location'] = st.text_input("Enter Address of Institute", value=st.session_state.d['education']['location'])
            education['duration'] = st.text_input("Enter duration in format 2019-2023", value=st.session_state.d['education']['duration'])

        st.session_state.d['education'] = education
        st.markdown('---')
        
        
        #####Project Info#####

        
        # st.subheader("Project Details")
        
        if "show_project_form" not in st.session_state:
            st.session_state.show_project_form = False

        if st.button("Add Project"):
            st.session_state.show_project_form = True

        if st.session_state.show_project_form:
            self.add_project()
            

        self.display_projects()
                
                

        
        if st.button("Create Resume"):
            st.write(st.session_state.d)
            # self.save_data()
            

