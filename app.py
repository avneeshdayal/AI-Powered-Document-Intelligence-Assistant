
import os
import streamlit as st
from dotenv import load_dotenv

from src.document_processor import extract_pages
from src.chunker import create_chunks
from src.retriever import index_chunks, retrieve
from src.generator import generate_answer

load_dotenv()

try:
    if "GEMINI_API_KEY" in st.secrets:
        os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

    if "GEMINI_CHAT_MODEL" in st.secrets:
        os.environ["GEMINI_CHAT_MODEL"] = st.secrets["GEMINI_CHAT_MODEL"]
except Exception:
    pass

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
:root {
    color-scheme: light;
}

[data-testid="stHeader"] {
    background: transparent;
}

.stApp,
[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
    color: #111827 !important;
}

.block-container {
    max-width: 850px;
    padding: 2rem 1.5rem 5rem;
}

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
    color: #111827;
}

[data-testid="stSidebar"] {
    display: none;
}

h1, h2, h3 {
    color: #111827 !important;
    letter-spacing: -0.4px;
}

[data-testid="stChatMessage"] {
    background: #ffffff !important;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 1rem;
}

[data-testid="stChatInput"] {
    background: #ffffff !important;
    border: 1px solid #d1d5db;
    border-radius: 12px;
}

[data-testid="stFileUploader"] section {
    background: #ffffff !important;
    border: 1px dashed #9ca3af !important;
    border-radius: 12px !important;
    padding: 1rem;
}

[data-testid="stFileUploader"] button {
    background: #ffffff !important;
    color: #1d4ed8 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 8px !important;
}

.stButton > button {
    min-height: 42px;
    background: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #2563eb !important;
    border-radius: 9px !important;
    font-weight: 600;
    box-shadow: none !important;
}

.stButton > button:hover {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
}

.stButton > button:disabled {
    background: #e5e7eb !important;
    color: #6b7280 !important;
    border-color: #e5e7eb !important;
}

[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #e5e7eb !important;
}

.small-note {
    color: #6b7280;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

defaults = {
    "collection": None,
    "chat_history": [],
    "indexed_files": [],
    "indexed_chunks": 0,
    "index_signature": None,
    "pending_question": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("AI Document Assistant")

st.markdown(
    "<p class='small-note'>"
    "Upload PDFs, ask questions, and explore your documents "
    "</p>",
    unsafe_allow_html=True,
)

st.divider()

if not os.getenv("GEMINI_API_KEY"):
    st.error(
        "GEMINI_API_KEY is missing. Add it to your .env file "
        "and restart the application."
    )
    st.stop()

st.subheader("Upload documents")

st.caption(
    "Choose one or more PDF files to create your searchable "
    "document collection."
)

file_uploads = st.file_uploader(
    "Choose PDF files",
    type=["pdf"],
    accept_multiple_files=True,
    key="document_files",
    help="You can upload multiple PDF documents.",
)

all_uploads = []
seen_uploads = set()

for uploaded in file_uploads or []:
    signature = (uploaded.name, len(uploaded.getvalue()))

    if signature not in seen_uploads:
        seen_uploads.add(signature)
        all_uploads.append(uploaded)

current_signature = (
    tuple(
        (f.name, len(f.getvalue()))
        for f in all_uploads
    )
    if all_uploads else None
)

if all_uploads:
    st.caption(f"{len(all_uploads)} PDF file(s) selected")

    with st.expander("View selected files"):
        for uploaded in all_uploads:
            st.markdown(f"- 📄 {uploaded.name}")


if st.button(
    "Process documents",
    use_container_width=True,
    disabled=not all_uploads,
    key="process_documents",
):
    try:
        with st.spinner(
            "Reading PDFs and preparing your document index..."
        ):
            pages = []
            file_names = []

            for uploaded in all_uploads:
                file_names.append(uploaded.name)

                pages.extend(
                    extract_pages(
                        uploaded.getvalue(),
                        uploaded.name,
                    )
                )

            chunks = create_chunks(pages)

            if not chunks:
                st.error(
                    "No readable text was found. "
                    "If your PDFs contain scanned pages, OCR may be needed."
                )
            else:
                collection = index_chunks(chunks)

                st.session_state.collection = collection
                st.session_state.indexed_files = file_names
                st.session_state.indexed_chunks = len(chunks)
                st.session_state.index_signature = current_signature
                st.session_state.chat_history = []
                st.session_state.pending_question = None

                st.rerun()

    except Exception as exc:
        st.error(f"Could not process documents: {exc}")

if st.session_state.collection is not None:

    st.divider()

    st.subheader("Your document workspace")

    st.success(
        f"{len(st.session_state.indexed_files)} document(s) ready "
        f"· {st.session_state.indexed_chunks} searchable chunks"
    )

    with st.expander("View indexed documents"):
        for name in st.session_state.indexed_files:
            st.markdown(f"📄 **{name}**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "Clear chat",
            use_container_width=True,
        ):
            st.session_state.chat_history = []
            st.session_state.pending_question = None
            st.rerun()

    with col2:
        if st.button(
            "Remove document index",
            use_container_width=True,
        ):
            st.session_state.collection = None
            st.session_state.chat_history = []
            st.session_state.indexed_files = []
            st.session_state.indexed_chunks = 0
            st.session_state.index_signature = None
            st.session_state.pending_question = None
            st.rerun()

    st.subheader("Quick actions")

    if st.button(
        "Summarize documents",
        use_container_width=True,
    ):
        st.session_state.pending_question = (
            "Provide a clear summary of the uploaded documents. "
            "Organize the answer into an overview, key findings, "
            "important facts, and conclusions. Use only the "
            "provided passages. Identify any limitations in the "
            "available evidence."
        )
        st.rerun()

    st.markdown("#### Try asking")

    suggestions = [
        "Summarize the main points",
        "What are the key findings?",
        "What risks or challenges are mentioned?",
    ]

    suggestion_columns = st.columns(3)

    for i, suggestion in enumerate(suggestions):
        with suggestion_columns[i]:
            if st.button(
                suggestion,
                key=f"suggestion_{i}",
                use_container_width=True,
            ):
                st.session_state.pending_question = suggestion
                st.rerun()

    st.divider()

    st.subheader("Chat with your documents")

    for turn in st.session_state.chat_history:

        with st.chat_message("user"):
            st.markdown(turn["question"])

        with st.chat_message("assistant"):
            st.markdown(turn["answer"])

            sources = turn.get("sources", [])

            if sources:
                with st.expander(
                    f"Sources ({len(sources)})"
                ):
                    for source in sources:
                        st.markdown(
                            f"**{source.get('source', 'Document')} "
                            f"· Page {source.get('page', '?')}**"
                        )

                        st.caption(source.get("text", ""))


    question = st.chat_input(
        "Ask a question about your PDFs..."
    )

    if question and question.strip():
        st.session_state.pending_question = question.strip()


    pending_question = st.session_state.pending_question

    if pending_question:
        # Clear the pending value before processing to prevent
        # the same question from being processed repeatedly.
        st.session_state.pending_question = None

        with st.chat_message("user"):
            st.markdown(pending_question)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and preparing an answer..."):

                try:
                    recent_turns = (
                        st.session_state.chat_history[-4:]
                    )

                    conversation_context = "\n".join(
                        f"User: {turn['question']}\n"
                        f"Assistant: {turn['answer']}"
                        for turn in recent_turns
                    )

                    retrieval_query = (
                        f"{conversation_context}\n"
                        f"Current question: {pending_question}"
                        if conversation_context
                        else pending_question
                    )

                    passages = retrieve(
                        st.session_state.collection,
                        retrieval_query,
                        top_k=4,
                    )

                    prompt_question = (
                        f"Previous conversation:\n"
                        f"{conversation_context}\n\n"
                        f"Current question: {pending_question}\n\n"
                        "Answer the current question using only "
                        "the provided document passages. Use prior "
                        "conversation only to resolve references. "
                        "If the passages do not contain enough "
                        "information, say so clearly. Do not invent "
                        "facts or citations."
                        if conversation_context
                        else (
                            f"{pending_question}\n\n"
                            "Answer using only the provided document "
                            "passages. If they do not contain enough "
                            "information, say so clearly. Do not "
                            "invent facts or citations."
                        )
                    )

                    answer = generate_answer(
                        prompt_question,
                        passages,
                    )

                    # Remove duplicate source passages.
                    unique_sources = []
                    seen_sources = set()

                    for passage in passages:
                        key = (
                            passage.get("source"),
                            passage.get("page"),
                            passage.get("text"),
                        )

                        if key not in seen_sources:
                            seen_sources.add(key)
                            unique_sources.append(passage)

                    st.markdown(answer)

                    if unique_sources:
                        with st.expander(
                            f"Sources ({len(unique_sources)})"
                        ):
                            for source in unique_sources:
                                st.markdown(
                                    f"**{source.get('source', 'Document')} "
                                    f"· Page {source.get('page', '?')}**"
                                )

                                st.caption(
                                    source.get("text", "")
                                )

                    st.session_state.chat_history.append({
                        "question": pending_question,
                        "answer": answer,
                        "sources": unique_sources,
                    })

                except Exception as exc:
                    error_message = (
                        f"Could not answer the question: {exc}"
                    )

                    st.error(error_message)

                    st.session_state.chat_history.append({
                        "question": pending_question,
                        "answer": error_message,
                        "sources": [],
                    })

else:

    st.divider()

    st.markdown(
        "<div style='text-align:center; padding: 1.5rem 0;'>"
        "<p style='font-size: 2rem; margin-bottom: 0.5rem;'>📄</p>"
        "<p style='font-weight:600; font-size:1.1rem; "
        "color:#111827;'>Your documents, ready to explore</p>"
        "<p style='color:#6b7280;'>"
        "Upload your PDFs above and click "
        "'Process documents' to get started."
        "</p></div>",
        unsafe_allow_html=True,
    )
