from pypdf import PdfReader
import os
from  dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class User_Info_Extractor:
    
    def __init__(self):
        self.api_key = os.environ.get("OPEN_API_KEY")
        self.base_url = os.environ.get("BASE_URL")
        self.model_name = os.environ.get("MODEL_NAME")
        self.client = OpenAI(api_key=self.api_key,
                             base_url=self.base_url                             
                             )
    
    def create_prompt(self,text):
        with open("extract_prompt.txt",'r') as file:
            prompt = file.read()
            
            prompt += text
        return prompt
        
 
    
    def extract_user_info(self,file):
        
        
        reader = PdfReader(file)
        
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        response = self.client.chat.completions.create(
            model= self.model_name,
            messages=[
                {
                    'role':"user",
                    "content" : self.create_prompt(text)
                }
            ]
        )    
            
        
        return response.choices[0].message.content