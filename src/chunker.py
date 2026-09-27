def create_chunks(pages, chunk_size=1000, overlap=150):
    chunks = []
    for page in pages:
        text = page["text"]
        start, chunk_id = 0, 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append({"text": chunk_text, "page": page["page"], "chunk_id": chunk_id})
            chunk_id += 1
            if end >= len(text):
                break
            start = end - overlap
    return chunks
