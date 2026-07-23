
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
        self.model=os.environ.get("MODEL_NAME")
        self.client = OpenAI(api_key= self.api_key
                    ,base_url=self.base_url
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

    def create_resume(self, output_file="resume.pdf"):
        
        
        response = self.client.chat.completions.create(
            model = self.model,
            messages=[
                {
                    "role": "user",
                    "content": self.create_prompt()
                }
            ]
        )

        data = (response.choices[0].message.content)
        data = data.replace("```json", "")
        data = data.replace("```", "")
        data = data.strip()
        # print("=================================================================")
        # print(data)
        # print("=================================================================")
        try:
            resume = json.loads(data)
        except json.JSONDecodeError:
            print("Invalid JSON returned:")
            print(data)
            return

        obj = ResumePDFBuilder(resume=resume,output_file=output_file)

        obj.create()

        # print(response)

