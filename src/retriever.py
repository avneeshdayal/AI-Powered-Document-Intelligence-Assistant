
import os
import chromadb
from google import genai
from google.genai import types

# Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing. Configure it in .env or Streamlit Secrets.")

gemini_client = genai.Client(api_key=api_key)

# In-memory ChromaDB client
chroma_client = chromadb.Client()


def embed_texts(texts):
    """Generate embeddings for a list of text chunks."""
    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [item.values for item in response.embeddings]


def embed_query(query):
    """Generate an embedding for a user question."""
    response = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return response.embeddings[0].values


def index_chunks(chunks):
    """Index document chunks in ChromaDB."""
    collection = chroma_client.get_or_create_collection(
        name="document_chunks"
    )

    # Clear old entries before indexing a new document set
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"chunk_{i}")
        documents.append(chunk["text"])
        metadatas.append({
            "source": chunk["source"],
            "page": int(chunk["page"]),
        })

    if documents:
        embeddings = embed_texts(documents)
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    return collection


def retrieve(collection, question, top_k=4):
    """Retrieve the most relevant document chunks."""
    query_embedding = embed_query(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    passages = []
    for text, metadata in zip(
        results["documents"][0],
        results["metadatas"][0],
    ):
        passages.append({
            "text": text,
            "source": metadata["source"],
            "page": metadata["page"],
        })

    return passages
