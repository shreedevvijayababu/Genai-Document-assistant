from app.core.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks suitable for embedding."""
    text = text.strip()
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += size - overlap
    return chunks
