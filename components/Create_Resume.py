
import os
from openai import OpenAI
from dotenv import load_dotenv
from components.Resume_pdf import ResumePDFBuilder
import json




load_dotenv()

class Create_Resume:
    def __init__(self,user_info,job_description):
        self.api_key=os.environ.get("OPENAI_API_KEY")
        self.base_url=os.environ.get("BASE_URL")
        self.model_name=os.environ.get("MODEL_NAME")
        self.client = OpenAI(api_key= self.api_key,
                    base_url=self.base_url
                    )
        self.user_info = user_info
        
        
        
        self.job_description = job_description
        
    

    def create_prompt(self,file_path="prompt.txt"):
            
        with open(file_path,'r') as file:
            text = file.read()
            text += "Candidate Details \n"
            text += json.dumps(self.user_info, indent=2)
            text+= "\nJob Description"
            text+= self.job_description
            
            return text

    def create_resume(self, output_file):
        
        
        response = self.client.chat.completions.create(
            model = self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": self.create_prompt()
                }
            ]
        )
        
        
        # print("=================================================================")
        # print(type(response.choices[0].message.content))
        # print("=================================================================")
        
        
      

        data = (response.choices[0].message.content)
        data = data.replace("```json", "")
        data = data.replace("```", "")
        data = data.strip()
        try:
            resume = json.loads(data)
        except json.JSONDecodeError:
            print("Invalid JSON returned:")
            print(data)
            return

        builder = ResumePDFBuilder(resume=resume,output_file=output_file)

        pdf_file = builder.create()
        
        
        return pdf_file

        # print(response)

