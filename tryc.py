import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api= os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api)
model=genai.GenerativeModel("gemini-2.5-flash")
response= model.generate_content('What is RAG?')
print(response.text)