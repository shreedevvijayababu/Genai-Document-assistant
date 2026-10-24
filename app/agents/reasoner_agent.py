from app.services.rag_service import generate_answer


def run(question, chunks):
    """Reasoner agent: draft a grounded answer from the retrieved chunks."""
    return generate_answer(question, chunks)
