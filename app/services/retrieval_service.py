from app.api import llm_client
from app.services import vector_store
from app.core.config import TOP_K


def retrieve(query, k=TOP_K):
    """Find the document chunks most similar to the query."""
    if vector_store.count() == 0:
        return []
    return vector_store.search(llm_client.embed([query], input_type="search_query")[0], k)
