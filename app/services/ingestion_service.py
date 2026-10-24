import io
import pandas as pd
from pypdf import PdfReader


def read_file(filename, data):
    """Extract plain text from a PDF, TXT, CSV or XLSX file (bytes)."""
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "pdf":
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    if ext == "txt":
        return data.decode("utf-8", errors="ignore")
    if ext == "csv":
        return pd.read_csv(io.BytesIO(data)).to_csv(index=False)
    if ext == "xlsx":
        sheets = pd.read_excel(io.BytesIO(data), sheet_name=None)
        return "\n\n".join(f"Sheet: {name}\n{df.to_csv(index=False)}" for name, df in sheets.items())
    raise ValueError(f"Unsupported file type: .{ext}")
