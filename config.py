import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("Missing API_KEY")

genai.configure(api_key=API_KEY)

model= "gemini-2.5-flash"
chroma = "chroma_db"

top_k= 3
max_context = 2500