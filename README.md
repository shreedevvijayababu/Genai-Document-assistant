# Document Assistant: Agentic RAG (Generative AI Capstone)

A Streamlit app where users upload documents (PDF, TXT, CSV, Excel) and ask natural-language questions. A team of AI agents plans the search, retrieves relevant passages from a vector database, drafts an answer with an LLM, and validates that the answer is grounded in the documents.

## Features
- Multi-format ingestion: PDF, TXT, CSV, XLSX
- Semantic search with Cohere embeddings stored in ChromaDB
- Retrieval-Augmented Generation (answers use only retrieved context)
- Four cooperating agents: Planner, Retriever, Reasoner, Validator
- Guardrails: input validation, file checks, prompt-injection blocklist, error handling, hallucination check

## Setup
1. Install Python 3.10+.
2. Create a virtual environment and activate it:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set `COHERE_API_KEY` (free trial key from dashboard.cohere.com).
5. `streamlit run main.py`

## How to use
1. Upload one or more files and click **Index documents**.
2. Type a question and click **Ask**.
3. Read the answer, the source files, and the validator verdict. Open **Agent trace** to see the planner's search query.
4. **Clear knowledge base** removes all indexed documents.

## Architecture
```
Upload -> ingestion_service (extract text) -> chunking_service (1000-char chunks, 150 overlap)
       -> llm_client.embed (Cohere embeddings) -> vector_store (ChromaDB, cosine similarity)

Question -> guardrails -> Planner -> Retriever -> Reasoner -> Validator -> Answer + sources
```

| Folder / file | Purpose |
|---|---|
| `main.py` | Streamlit interface |
| `app/core/config.py` | Settings (models, chunk size, limits) |
| `app/api/llm_client.py` | Cohere connection (embeddings and text generation) |
| `app/services/` | Ingestion, chunking, vector store, retrieval, RAG answer generation |
| `app/agents/` | The four agents and the orchestrator that chains them |
| `app/utils/` | Guardrails and upload-handling helper |

## Agent roles
- **Planner**: rewrites the user's question into a short, focused search query (falls back to the original question on error).
- **Retriever**: embeds the query and fetches the top 5 most similar chunks from ChromaDB.
- **Reasoner**: builds a prompt from the retrieved chunks and drafts an answer using only that context, citing source files.
- **Validator**: acts as a fact-checker and labels the answer SUPPORTED or UNSUPPORTED. Unsupported answers are shown with a warning.

## Reliability and safety
- Empty, oversized (over 1000 characters), or prompt-injection style questions are rejected.
- Files must be PDF/TXT/CSV/XLSX and under 10 MB; unreadable files report an error instead of crashing.
- The prompt instructs the model to say when the answer is not in the documents.
- All agent calls are wrapped in error handling in the UI.

## Deployment (Streamlit Community Cloud)
1. Push the project to a public GitHub repo (`.env` must NOT be included).
2. Go to share.streamlit.io, click **New app**, and select the repo, branch `main`, and file `main.py`.
3. Under **Advanced settings > Secrets**, add: `COHERE_API_KEY = "your_key"`.
4. Deploy. The app gets a public URL.

## Limitations
- Chunking is character-based, so a chunk can cut through a sentence or a table row.
- Scanned PDFs (images without a text layer) cannot be read; there is no OCR.
- The vector store on Streamlit Cloud is not permanent and resets when the app restarts.
- The validator is itself an LLM, so it reduces but does not eliminate hallucinations.
- Large spreadsheets are converted to text and may produce many chunks and slow indexing.
- The free Cohere trial key allows about 1,000 API calls per month and 20 chat calls per minute, so heavy use can be slowed or blocked. It is also intended for development, not commercial use.

## Challenges faced
The biggest challenges I faced were with setup rather than the code itself. Python wasn’t recognized in the VS Code terminal, and I eventually realized it was already installed through Anaconda, so I created a dedicated Python 3.12 environment in Anaconda Prompt and ran the project from there. The larger obstacle was the API key: Google AI Studio kept returning a “permission denied” error and showed no cloud projects, so I could not create a Gemini key. Because the project keeps all AI calls in a single file, I was able to switch to Cohere by changing the client, the model names, and the dependencies, while the ingestion, vector store, and agents stayed the same. After the switch, I tested the app with a small document, confirmed that answers cited their sources, and confirmed that questions outside the document were declined. The free Cohere trial key also has monthly call limits, which I noted as a limitation of the deployment.
