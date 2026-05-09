import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from config import chroma, model, top_k, max_context
from rate import rate_limit 
import os
from dotenv import load_dotenv
load_dotenv()

api=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=chroma)
collection = client.get_collection("knowledge")

def get_context(question):
    q_embedding = embed_model.encode(question).tolist()
    results = collection.query(query_embeddings=[q_embedding], n_results=top_k)
    docs = results["documents"][0]
    return docs, "\n\n".join(docs)[:max_context]

def generate_answer(question, context):
    rate_limit()
    prompt = f"Answer in less than 100 words using ONLY the context.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    
    gemini = genai.GenerativeModel(model)
    response = gemini.generate_content(prompt)
    return response.text

def ask(question):
    docs, context = get_context(question)
    answer = generate_answer(question, context)
    return answer, docs