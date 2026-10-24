from app.core.config import MAX_FILE_SIZE_MB, MAX_QUESTION_CHARS, SUPPORTED_FILE_TYPES

BLOCKED_PHRASES = ["ignore previous instructions", "ignore all instructions", "reveal your system prompt"]


def validate_question(question):
    """Return (ok, message). Blocks empty, oversized, or prompt-injection input."""
    q = (question or "").strip()
    if not q:
        return False, "Please type a question."
    if len(q) > MAX_QUESTION_CHARS:
        return False, f"Question is too long (max {MAX_QUESTION_CHARS} characters)."
    if any(p in q.lower() for p in BLOCKED_PHRASES):
        return False, "That request can't be processed."
    return True, ""


def validate_file(name, size_bytes):
    ext = name.rsplit(".", 1)[-1].lower()
    if ext not in SUPPORTED_FILE_TYPES:
        return False, f"{name}: unsupported file type."
    if size_bytes > MAX_FILE_SIZE_MB * 1024 * 1024:
        return False, f"{name}: larger than {MAX_FILE_SIZE_MB} MB."
    return True, ""
