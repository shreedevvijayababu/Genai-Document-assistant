import os
from app.api import llm_client
from app.services import vector_store
from app.services.ingestion_service import read_file
from app.services.chunking_service import chunk_text
from app.utils.guardrails import validate_file


def ingest_uploads(uploaded_files):
    """Read, chunk, embed and store each uploaded file. Returns (indexed_names, errors)."""
    os.makedirs("data", exist_ok=True)
    done, errors = [], []
    for f in uploaded_files:
        data = f.getvalue()
        ok, msg = validate_file(f.name, len(data))
        if not ok:
            errors.append(msg)
            continue
        try:
            chunks = chunk_text(read_file(f.name, data))
            if not chunks:
                errors.append(f"{f.name}: no readable text found.")
                continue
            vector_store.add_chunks(f.name, chunks, llm_client.embed(chunks))
            done.append(f"{f.name} ({len(chunks)} chunks)")
        except Exception as e:
            errors.append(f"{f.name}: {e}")
    return done, errors
