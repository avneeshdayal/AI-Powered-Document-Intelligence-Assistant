from src.chunker import create_chunks

def test_chunk_metadata():
    pages = [{"page": 2, "text": "A" * 1500}]
    chunks = create_chunks(pages)
    assert len(chunks) >= 2
    assert chunks[0]["page"] == 2
    assert "chunk_id" in chunks[0]
