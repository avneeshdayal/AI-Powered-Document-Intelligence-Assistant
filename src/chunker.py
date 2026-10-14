def create_chunks(pages, chunk_size=1200, overlap=200):
    chunks = []
    for page in pages:
        text = page["text"]
        start = 0
        while start < len(text):
            part = text[start:start + chunk_size].strip()
            if part:
                chunks.append({
                    "text": part,
                    "source": page["source"],
                    "page": page["page"],
                })
            if start + chunk_size >= len(text):
                break
            start += chunk_size - overlap
    return chunks
