import streamlit as st
from streamlit_local_storage import LocalStorage
import json
from components.Create_Resume import Create_Resume

class User_Info:
    
    def __init__(self):
        
        self.local_storage = LocalStorage()
        
        if 'd' not in st.session_state:
            data = self.load_data()
            if data:
                st.session_state.d = data
                st.session_state.projects = data['projects']
                st.session_state.d["certifications"] = data['certifications']
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
                    "education": [],
                    "projects": [],
                    "certifications" : []
                    }
                st.session_state.projects = []
                st.session_state.educations = []
                
                # for reference
                # education = {
                #         "institute_name": "",
                #         "degree_certificate_name": "",
                #         "location": "",
                #         "duration": ""
                #     }
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
        data = json.dumps(st.session_state.d)        # d is dictionary for whole user data
        
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
        
    def education_details(self, education, index):
        with st.form(key=f'education_{index}', clear_on_submit=False):
            college = st.text_input("Institute/College Name", value=education.get('college', ''))
            location = st.text_input("Location", value=education.get('location', ''))
            degree = st.text_input("Degree/Certificate Name", value=education.get('degree', ''))
            year = st.text_input("Duration/Year (e.g., 2019-2023)", value=education.get('year', ''))
            
            submitted = st.form_submit_button("Update Education")

            if submitted:
                st.session_state.educations[index] = {
                    "college": college,
                    "location": location,
                    "degree": degree,
                    "year": year
                }
                st.session_state.d['education'] = st.session_state.educations
                st.success("Education updated Successfully")
                st.rerun()
                
    def render_education_section(self):
        st.subheader("🎓 Education Details")

   
        if 'educations' not in st.session_state:
            st.session_state.educations = st.session_state.d.get('education', [])
            
        with st.expander("➕ Add New Education", expanded=False):
            with st.form(key="add_new_education", clear_on_submit=True):
                college = st.text_input("Institute/College Name")
                location = st.text_input("Location")
                degree = st.text_input("Degree/Certificate Name")
                year = st.text_input("Duration/Year (e.g., 2019-2023)")
                
                add_submitted = st.form_submit_button("Add Education")

                if add_submitted:
                    new_edu = {
                        "college": college,
                        "location": location,
                        "degree": degree,
                        "year": year
                    }
                    st.session_state.educations.append(new_edu)
                    st.session_state.d['education'] = st.session_state.educations
                    self.save_data()
                    st.success("Education added successfully!")
                    st.rerun()

        # Edit Existing Education Entries
        if st.session_state.educations:
            for idx, edu in enumerate(st.session_state.educations):
                with st.expander(f"🎓 {edu.get('college', f'Education #{idx+1}')}", expanded=False):
                    self.education_details(edu, idx)
                    
                    # Delete button for each item
                    if st.button("Delete Education", key=f"delete_edu_{idx}"):
                        st.session_state.educations.pop(idx)
                        st.session_state.d['education'] = st.session_state.educations
                        st.rerun()
    def project_details(self, project, index):
        """Form to edit an existing project."""
        with st.form(key=f'edit_project_form_{index}', clear_on_submit=False):
            title = st.text_input(
                "Project Title", 
                value=project.get('title', ''), 
                key=f"edit_proj_title_{index}"
            )
            tech_used = st.text_input(
                "Technologies Used", 
                value=project.get('tech_used', ''), 
                key=f"edit_proj_tech_{index}"
            )
            project_year = st.text_input(
                "Project Year", 
                value=project.get('project_year', ''), 
                key=f"edit_proj_year_{index}"
            )
            frontend_code_url = st.text_input(
                "Frontend Code URL", 
                value=project.get('frontend_code_url', ''), 
                key=f"edit_proj_fe_{index}"
            )
            backend_code_url = st.text_input(
                "Backend Code URL", 
                value=project.get('backend_code_url', ''), 
                key=f"edit_proj_be_{index}"
            )
            live_link = st.text_input(
                "Live Demo URL", 
                value=project.get('live_link', ''), 
                key=f"edit_proj_live_{index}"
            )
            description = st.text_area(
                "Enter your description",
                placeholder="Enter points separated with comma",
                value=project.get('description', ''),
                key=f"edit_proj_desc_{index}"
            )
            submitted = st.form_submit_button("Update Project")

            if submitted:
                st.session_state.projects[index] = {
                    "title": title,
                    "tech_used": tech_used,
                    "project_year": project_year,
                    "frontend_code_url": frontend_code_url,
                    "backend_code_url": backend_code_url,
                    "live_link": live_link,
                    "description": description
                }
                st.session_state.d['projects'] = st.session_state.projects
                st.session_state.edit_project = None  # Close edit form after saving
                self.save_data()  # Persist changes to local storage
                st.success("Project updated successfully!")
                st.rerun()

    def add_project(self):
        """Form to add a new project."""
        with st.form(key='add_project_form_unique', clear_on_submit=True):
            title = st.text_input("Project Title", key="new_proj_title")
            tech_used = st.text_input("Technologies Used", key="new_proj_tech")
            project_year = st.text_input("Project Year", key="new_proj_year")
            frontend_code_url = st.text_input("Frontend Code URL", key="new_proj_fe")
            backend_code_url = st.text_input("Backend Code URL", key="new_proj_be")
            live_link = st.text_input("Live Demo URL", key="new_proj_live")
            description = st.text_area(
                "Enter project description",
                placeholder="Enter points separated with comma",
                key="new_proj_desc"
            )
            submitted = st.form_submit_button("➕ Add Project")

            if submitted:
                if title.strip():
                    new_proj = {
                        "title": title,
                        "tech_used": tech_used,
                        "project_year": project_year,
                        "frontend_code_url": frontend_code_url,
                        "backend_code_url": backend_code_url,
                        "live_link": live_link,
                        "description": description
                    }
                    st.session_state.projects.append(new_proj)
                    st.session_state.d['projects'] = st.session_state.projects
                    st.session_state.show_project_form = False
                    self.save_data()  # Persist changes to local storage
                    st.success("Project added successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter a Project Title.")

    def display_projects(self):
        """Main rendering method for the Projects section."""
        st.subheader("🚀 Project Details")

        if "projects" not in st.session_state:
            st.session_state.projects = st.session_state.d.get("projects", [])

        if "edit_project" not in st.session_state:
            st.session_state.edit_project = None

        if len(st.session_state.projects) == 0:
            st.info("No projects added yet.")
            return

        for index, project in enumerate(st.session_state.projects):
            title_label = project.get('title') if project.get('title') else 'Untitled Project'
            
            with st.expander(f"{index+1}. {title_label}"):
                # If currently editing this specific project, show the edit form directly inside
                if st.session_state.edit_project == index:
                    st.markdown("#### ✏ Edit Project Details")
                    self.project_details(project, index)
                    
                    if st.button("Cancel Editing", key=f"cancel_edit_{index}"):
                        st.session_state.edit_project = None
                        st.rerun()
                else:
                    # Otherwise, show details and Edit/Delete buttons
                    st.write("**Title:**", project.get("title", ""))
                    st.write("**Technologies:**", project.get("tech_used", ""))
                    st.write("**Year:**", project.get("project_year", ""))
                    if project.get("frontend_code_url"):
                        st.write("**Frontend Code:**", project.get("frontend_code_url"))
                    if project.get("backend_code_url"):
                        st.write("**Backend Code:**", project.get("backend_code_url"))
                    if project.get("live_link"):
                        st.write("**Live Link:**", project.get("live_link"))
                    st.write("**Description:**", project.get("description", ""))

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✏ Edit", key=f"edit_btn_{index}"):
                            st.session_state.edit_project = index
                            st.rerun()

                    with col2:
                        if st.button("🗑 Delete", key=f"delete_btn_{index}"):
                            st.session_state.projects.pop(index)
                            st.session_state.d["projects"] = st.session_state.projects
                            if st.session_state.edit_project == index:
                                st.session_state.edit_project = None
                            self.save_data()  # Persist changes to local storage
                            st.success("Project deleted.")
                            st.rerun()
                
    def job_description(self):
        jd = st.text_area("Enter Job Description")
        
        st.session_state.jd = jd
    
    
  
    def certification_details(self, cert, index):
        """Form to edit an existing certification."""
        with st.form(key=f'edit_cert_form_{index}', clear_on_submit=False):
            name = st.text_input(
                "Certification Name",
                value=cert.get('name', ''),
                key=f"edit_cert_name_{index}"
            )
            issuer = st.text_input(
                "Issuer / Organization",
                value=cert.get('issuer', ''),
                key=f"edit_cert_issuer_{index}"
            )
            year = st.text_input(
                "Year",
                value=cert.get('year', ''),
                key=f"edit_cert_year_{index}"
            )
            url = st.text_input(
                "Credential URL (optional)",
                value=cert.get('credential_url', ''),
                key=f"edit_cert_url_{index}"
            )

            submitted = st.form_submit_button("Update Certification")

            if submitted:
                st.session_state.certifications[index] = {
                    "name": name,
                    "issuer": issuer,
                    "year": year,
                    "credential_url": url
                }
                st.session_state.d['certifications'] = st.session_state.certifications
                self.save_data()  # Persist changes to local storage
                st.success("Certification updated successfully!")
                st.rerun()

    def add_certification(self):
        """Form to add a new certification."""
        with st.form(key='add_cert_form_unique', clear_on_submit=True):
            name = st.text_input("Certification Name", key="new_cert_name")
            issuer = st.text_input("Issuer / Organization", key="new_cert_issuer")
            year = st.text_input("Year", key="new_cert_year")
            url = st.text_input("Credential URL (optional)", key="new_cert_url")

            submitted = st.form_submit_button("Add Certification")

            if submitted:
                if name.strip():
                    new_cert = {
                        "name": name,
                        "issuer": issuer,
                        "year": year,
                        "credential_url": url
                    }
                    st.session_state.certifications.append(new_cert)
                    st.session_state.d['certifications'] = st.session_state.certifications
                    st.session_state.show_cert_form = False
                    self.save_data()  # Persist changes to local storage
                    st.success("Certification added successfully!")
                    st.rerun()
                else:
                    st.warning("Please enter a Certification Name.")

    def certification(self):
        """Main rendering method for the Certifications section."""
        st.subheader("📜 Certifications")

        # Initialize session state lists defensively
        if 'certifications' not in st.session_state:
            st.session_state.certifications = st.session_state.d.get("certifications", [])

        # Clean string/dict items defensively if previous data was saved as simple strings
        cleaned_certs = []
        for item in st.session_state.certifications:
            if isinstance(item, str):
                cleaned_certs.append({"name": item, "issuer": "", "year": "", "credential_url": ""})
            elif isinstance(item, dict):
                cleaned_certs.append(item)
        st.session_state.certifications = cleaned_certs
        st.session_state.d['certifications'] = cleaned_certs

        # Toggle Add Form
        if "show_cert_form" not in st.session_state:
            st.session_state.show_cert_form = False

        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("➕ Add Certification", key="toggle_add_cert_btn"):
                st.session_state.show_cert_form = not st.session_state.show_cert_form

        if st.session_state.show_cert_form:
            self.add_certification()

        # Display and edit existing certifications
        if not st.session_state.certifications:
            st.info("No certifications added yet.")
        else:
            for idx, cert in enumerate(st.session_state.certifications):
                label = cert.get('name') if cert.get('name') else f"Certification #{idx+1}"
                with st.expander(f"📜 {label}", expanded=False):
                    self.certification_details(cert, idx)

                    if st.button("🗑 Delete Certification", key=f"delete_cert_btn_{idx}"):
                        st.session_state.certifications.pop(idx)
                        st.session_state.d['certifications'] = st.session_state.certifications
                        self.save_data()  # Persist changes to local storage
                        st.success("Certification deleted.")
                        st.rerun()

    
        
    def user_info(self):
        
        st.subheader("ℹ️ Enter your Details")
        
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

        st.subheader("⚡ Technical skills")
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

        self.render_education_section()
        
        st.markdown('---')
    
        if "show_project_form" not in st.session_state:
            st.session_state.show_project_form = False

        if st.button("➕ Add Project"):
            st.session_state.show_project_form = True

        if st.session_state.show_project_form:
            self.add_project()
            
        self.display_projects()
        
        
        self.certification()
        
        self.job_description()
        
                  
        if st.button("Create Resume"):
            
            
            # st.write(st.session_state.d)
            self.save_data()
            
             
            resume_creator = Create_Resume(st.session_state.d,st.session_state.jd)
            resume_creator.create_resume(
                output_file="Abz.pdf"
            )
