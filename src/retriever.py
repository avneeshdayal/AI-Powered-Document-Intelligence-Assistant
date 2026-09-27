import os
import chromadb
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
db = chromadb.Client()

def index_chunks(chunks):
    name = "b2b_document_assistant"
    try:
        db.delete_collection(name)
    except Exception:
        pass
    collection = db.create_collection(name=name)
    ids = [f"{c['source']}_{c['page']}_{c['chunk_id']}" for c in chunks]
    collection.add(
        ids=ids,
        documents=[c["text"] for c in chunks],
        metadatas=[{"source": c["source"], "page": c["page"], "chunk_id": c["chunk_id"]} for c in chunks]
    )
    return collection

def retrieve(collection, question, top_k=5):
    r = collection.query(query_texts=[question], n_results=top_k)
    docs = r.get("documents", [[]])[0]
    metas = r.get("metadatas", [[]])[0]
    distances = r.get("distances", [[]])[0]
    return [
        {"text": d, "metadata": m, "distance": dist}
        for d, m, dist in zip(docs, metas, distances)
    ]
