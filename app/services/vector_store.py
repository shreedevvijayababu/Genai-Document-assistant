import uuid
import chromadb
from app.core.config import CHROMA_DIR

_collection = None


def _get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = client.get_or_create_collection("documents", metadata={"hnsw:space": "cosine"})
    return _collection


def add_chunks(source, chunks, embeddings):
    _get_collection().add(
        ids=[str(uuid.uuid4()) for _ in chunks],
        documents=chunks,
        embeddings=embeddings,
        metadatas=[{"source": source, "chunk": i} for i in range(len(chunks))],
    )


def search(query_embedding, k):
    res = _get_collection().query(query_embeddings=[query_embedding], n_results=k)
    return [
        {"text": t, "source": m["source"], "distance": d}
        for t, m, d in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def count():
    return _get_collection().count()


def reset():
    global _collection
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    try:
        client.delete_collection("documents")
    except Exception:
        pass
    _collection = None
