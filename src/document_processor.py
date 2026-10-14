from io import BytesIO
from pypdf import PdfReader

def extract_pages(pdf_bytes: bytes, filename: str):
    reader = PdfReader(BytesIO(pdf_bytes))
    pages = []
    for number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append({"text": text, "source": filename, "page": number})
    return pages
