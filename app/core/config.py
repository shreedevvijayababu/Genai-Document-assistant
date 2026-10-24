import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
LLM_MODEL = "command-a-03-2025"
EMBED_MODEL = "embed-v4.0"

SUPPORTED_FILE_TYPES = ["pdf", "txt", "csv", "xlsx"]
MAX_FILE_SIZE_MB = 10
MAX_QUESTION_CHARS = 1000

CHUNK_SIZE = 1000      # characters per chunk
CHUNK_OVERLAP = 150    # characters shared between neighbouring chunks
TOP_K = 5              # chunks retrieved per question

DATA_DIR = "data"
CHROMA_DIR = os.path.join(DATA_DIR, "chroma")
