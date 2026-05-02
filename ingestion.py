import chromadb
from sentence_transformers import SentenceTransformer
from config import chroma

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text):
    return embed_model.encode(text).tolist()

def chunk_text(text, size=150):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

with open("data/docs.txt") as f:
    text = f.read()

chunks = chunk_text(text)

client = chromadb.Client(
    chromadb.config.Settings(persist_directory=chroma)
)

collection = client.get_or_create_collection("knowledge")

for i, chunk in enumerate(chunks):
    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embed(chunk)]
    )

client.persist()
print("DB created")