import os
import time
import streamlit as st
from dotenv import load_dotenv
from src.document_processor import extract_pages
from src.chunker import create_chunks
from src.retriever import index_chunks, retrieve
from src.generator import generate_answer

load_dotenv()
st.set_page_config(page_title="B2B Document Intelligence Assistant", page_icon="📄", layout="wide")
st.title("📄 AI-Powered B2B Document Intelligence Assistant")
st.caption("RAG-based assistant for querying product, supplier and business documents with source citations.")

with st.sidebar:
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
    top_k = st.slider("Retrieved chunks", 2, 8, 5)

if "collection" not in st.session_state:
    st.session_state.collection = None

if uploaded_files and st.button("Index Documents"):
    all_chunks = []
    for uploaded in uploaded_files:
        path = os.path.join("data", uploaded.name)
        os.makedirs("data", exist_ok=True)
        with open(path, "wb") as f:
            f.write(uploaded.getbuffer())
        pages = extract_pages(path)
        chunks = create_chunks(pages)
        for c in chunks:
            c["source"] = uploaded.name
        all_chunks.extend(chunks)
    st.session_state.collection = index_chunks(all_chunks)
    st.success(f"Indexed {len(all_chunks)} chunks from {len(uploaded_files)} document(s).")

if st.session_state.collection:
    st.subheader("Ask a question")
    question = st.text_input("Example: What is the MOQ for stainless steel bottles?")
    if st.button("Ask") and question.strip():
        start = time.perf_counter()
        results = retrieve(st.session_state.collection, question, top_k)
        if not results:
            st.warning("I could not find sufficient information in the uploaded documents.")
        else:
            answer = generate_answer(question, results)
            latency = time.perf_counter() - start
            st.markdown("### Answer")
            st.write(answer["answer"])
            st.markdown("### Sources")
            for s in answer["sources"]:
                st.write(f"📄 {s['document']} — Page {s['page']}")
            st.caption(f"Response time: {latency:.2f} seconds | Retrieved chunks: {len(results)}")
            st.divider()
            st.write("Was this answer helpful?")
            c1, c2 = st.columns(2)
            if c1.button("👍 Yes"):
                st.info("Feedback recorded for the MVP.")
            if c2.button("👎 No"):
                st.info("Feedback recorded for retrieval/prompt improvement.")
else:
    st.info("Upload one or more PDFs and click 'Index Documents' to begin.")
