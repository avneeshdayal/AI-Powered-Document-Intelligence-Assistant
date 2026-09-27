# AI-Powered-Document-Intelligence-Assistant

A RAG-based AI application for querying product, supplier and business documents using natural language.

## Problem
B2B users often need to search across multiple documents to identify product specifications, supplier terms and delivery conditions.

## Solution
The application uses Retrieval-Augmented Generation to ingest PDFs, preserve page metadata, retrieve relevant context and generate grounded answers with source references.

## Key Features
- Multi-PDF ingestion
- Page-aware extraction and chunking
- Vector retrieval with ChromaDB
- LLM-based grounded answers
- Document/page source display
- Unsupported-query handling
- Basic latency tracking
- Evaluation-ready structure

## Product Workflow
PDF Upload → Page Extraction → Chunking → Vector Search → Retrieval → LLM → Answer + Sources

## Target Users
- Procurement teams
- B2B buyers
- Operations teams
- Sales teams

## Tech Stack
Python, Streamlit, OpenAI, ChromaDB, PyPDF, Pydantic

## Example Questions
- What is the minimum order quantity?
- Does a supplier offer customization?
- What is the delivery timeline?
- What are the payment terms?

## Project Structure
```text
ai-b2b-document-intelligence/
├── app.py
├── src/
├── evaluation/
├── docs/
├── data/sample/
├── tests/
├── requirements.txt
└── README.md
```

## Setup
```bash
pip install -r requirements.txt
```
Create `.env` from `.env.example`, add your OpenAI API key, then:
```bash
streamlit run app.py
```

## Future Scope
- Retrieval reranking
- Automated RAG evaluation
- Query routing / agentic workflows
- Supplier comparison
- Automated buyer enquiry generation
- Persistent feedback analytics
