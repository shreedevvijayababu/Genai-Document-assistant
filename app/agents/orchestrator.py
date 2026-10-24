from app.agents import planner_agent, retriever_agent, reasoner_agent, validator_agent

NOT_FOUND = "I couldn't find relevant information in the uploaded documents."


def answer_question(question):
    """Run plan -> retrieve -> reason -> validate and return a result dict."""
    search_query = planner_agent.plan(question)
    chunks = retriever_agent.run(search_query)
    if not chunks:
        return {"answer": NOT_FOUND, "sources": [], "validated": False, "query": search_query}
    answer = reasoner_agent.run(question, chunks)
    validated = validator_agent.run(question, answer, chunks)
    if not validated:
        answer = ("Warning: this answer could not be fully verified against your documents.\n\n" + answer)
    return {
        "answer": answer,
        "sources": sorted({c["source"] for c in chunks}),
        "validated": validated,
        "query": search_query,
    }
