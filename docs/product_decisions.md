# Product Decisions

## Why RAG?
The assistant needs answers grounded in user-provided business documents.

## Why page metadata?
Page-level metadata improves traceability and lets users verify answers against source material.

## Why an abstention path?
A document assistant should avoid presenting unsupported information as fact when evidence is unavailable.

## Future trade-offs
A production version could introduce reranking, caching, persistent vector storage, table extraction and model routing depending on quality, latency and cost.
