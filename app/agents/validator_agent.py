from app.api import llm_client
from app.services.rag_service import build_context


def run(question, answer, chunks):
    """Validator agent: check the answer is supported by the context."""
    prompt = (
        "You are a strict fact-checker. Is every claim in the ANSWER supported by the CONTEXT? "
        "Reply with exactly one word: SUPPORTED or UNSUPPORTED.\n\n"
        f"CONTEXT:\n{build_context(chunks)}\n\nQUESTION: {question}\n\nANSWER: {answer}"
    )
    verdict = llm_client.generate(prompt).upper()
    return "UNSUPPORTED" not in verdict and "SUPPORTED" in verdict
