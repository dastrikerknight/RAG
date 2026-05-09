import chromadb
from sentence_transformers import SentenceTransformer
from config import chroma

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, size=150):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size]).strip()
        if len(chunk) > 20:
            chunks.append(chunk)
    return chunks

try:
    with open("data/docs.txt",encoding="utf-8") as f:
        text = f.read()
except FileNotFoundError:
    raise ValueError("docs.txt not found in data/")
except UnicodeDecodeError:
    with open("data/docs.txt",encoding="latin-1") as f:
        text=f.read()

chunks = chunk_text(text)

client = chromadb.PersistentClient(path=chroma)
collection = client.get_or_create_collection("knowledge")

if collection.count() > 0:
    print("DB already exists. Skipping ingestion.")
else:
    embeddings = embed_model.encode(chunks).tolist()
    for i, chunk in enumerate(chunks):
        collection.add(
            ids=[str(i)],
            documents=[chunk],
            embeddings=[embeddings[i]],
            metadatas=[{"source": "docs.txt", "chunk_id": i}]
        )
    print("DB created successfully")