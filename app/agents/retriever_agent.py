from app.services.retrieval_service import retrieve


def run(search_query):
    """Retriever agent: fetch the most relevant chunks from the vector store."""
    return retrieve(search_query)
