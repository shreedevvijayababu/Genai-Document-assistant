from app.api import llm_client


def build_context(chunks):
    return "\n\n".join(f"[Source: {c['source']}]\n{c['text']}" for c in chunks)


def generate_answer(question, chunks):
    """Answer using ONLY the retrieved context (grounded generation)."""
    prompt = (
        "You are a document assistant. Answer the question using ONLY the context below. "
        "If the context does not contain the answer, say you could not find it in the documents. "
        "Mention the source file names you used.\n\n"
        f"Context:\n{build_context(chunks)}\n\nQuestion: {question}\n\nAnswer:"
    )
    return llm_client.generate(prompt)
