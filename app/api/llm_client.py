import cohere
from app.core.config import COHERE_API_KEY, LLM_MODEL, EMBED_MODEL

_client = None


def _get_client():
    global _client
    if _client is None:
        if not COHERE_API_KEY:
            raise RuntimeError("COHERE_API_KEY is missing. Add it to your .env file.")
        _client = cohere.ClientV2(api_key=COHERE_API_KEY)
    return _client


def embed(texts, input_type="search_document"):
    """Turn a list of strings into embedding vectors.
    Use input_type='search_query' for questions and 'search_document' for file chunks."""
    vectors = []
    for i in range(0, len(texts), 90):
        batch = texts[i:i + 90]
        response = _get_client().embed(
            texts=batch,
            model=EMBED_MODEL,
            input_type=input_type,
            embedding_types=["float"],
        )
        vectors.extend(response.embeddings.float_)
    return vectors


def generate(prompt):
    """Send a prompt to the LLM and return the text reply."""
    response = _get_client().chat(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.message.content[0].text.strip()
