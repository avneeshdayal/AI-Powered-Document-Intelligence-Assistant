import os
import uuid
import chromadb
from openai import OpenAI

def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY is missing from .env.")
    return OpenAI(
        api_key=key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

def _embed(texts):
    result = _client().embeddings.create(
        model="gemini-embedding-001",
        input=texts,
    )
    return [item.embedding for item in result.data]

def index_chunks(chunks):
    if not chunks:
        raise ValueError("No text was extracted from the PDFs.")
    client = chromadb.Client()
    collection = client.create_collection(name=f"pdf_{uuid.uuid4().hex[:12]}")
    texts = [c["text"] for c in chunks]
    vectors = _embed(texts)
    collection.add(
        ids=[str(i) for i in range(len(chunks))],
        documents=texts,
        embeddings=vectors,
        metadatas=[{"source": c["source"], "page": int(c["page"])} for c in chunks],
    )
    return collection

def retrieve(collection, question, top_k=4):
    count = collection.count()
    if count == 0:
        return []
    vector = _embed([question])[0]
    result = collection.query(
        query_embeddings=[vector],
        n_results=min(top_k, count),
        include=["documents", "metadatas", "distances"],
    )
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    return [
        {"text": d, "source": m.get("source", "Unknown"),
         "page": m.get("page", 0), "distance": dist}
        for d, m, dist in zip(docs, metas, distances)
    ]
