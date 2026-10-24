from app.api import llm_client


def plan(question):
    """Planner agent: rewrite the question into a short, focused search query."""
    prompt = (
        "Rewrite this question as a short search query for finding it in documents. "
        f"Return only the query, nothing else.\n\nQuestion: {question}"
    )
    try:
        return llm_client.generate(prompt) or question
    except Exception:
        return question
