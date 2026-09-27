# System Architecture

```text
User
 |
 v
Streamlit UI
 |
 +--> PDF Upload --> Page Extraction --> Chunking --> ChromaDB
 |
 +--> User Query --> Vector Retrieval --> Relevant Context
                                      |
                                      v
                               LLM Generation
                                      |
                                      v
                            Answer + Page Sources
                                      |
                                      v
                              User Feedback
```

Design principles:
- Preserve source metadata throughout ingestion.
- Ground answers in retrieved context.
- Return source pages for traceability.
- Separate retrieval from generation.
- Measure latency before optimizing.
