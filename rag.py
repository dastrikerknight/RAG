import chromadb
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from config import chroma, model, top_k, max_context
from utils import rate_limit

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text):
    return embed_model.encode(text).tolist()

client = chromadb.Client(
    chromadb.config.Settings(persist_directory=chroma)
)

collection = client.get_collection("knowledge")


def get_context(question):
    q_embedding = embed_text(question)

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=top_k
    )

    docs = results["documents"][0]
    context = "\n\n".join(docs)

    return docs, context[:max_context]


def generate_answer(question, context):
    rate_limit()

    prompt = f"""
Answer in less than 100 words.
Use ONLY the context.

Context:
{context}

Question:
{question}
"""

    model = genai.GenerativeModel(model)
    response = model.generate_content(prompt)

    return response.text


def ask(question):
    docs, context = get_context(question)
    answer = generate_answer(question, context)
    return answer, docs