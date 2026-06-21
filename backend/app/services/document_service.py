from pathlib import Path

import fitz
from docx import Document
from fastapi import UploadFile


async def extract_text_from_upload(file: UploadFile) -> tuple[str, str]:
    filename = file.filename or "uploaded_document"
    content = await file.read()
    suffix = Path(filename).suffix.lower()

    if suffix == ".pdf":
        with fitz.open(stream=content, filetype="pdf") as document:
            text = "\n".join(page.get_text() for page in document)
    elif suffix == ".docx":
        temp_path = Path(".tmp") / filename
        temp_path.parent.mkdir(exist_ok=True)
        temp_path.write_bytes(content)
        try:
            text = "\n".join(paragraph.text for paragraph in Document(temp_path).paragraphs)
        finally:
            temp_path.unlink(missing_ok=True)
    else:
        text = content.decode("utf-8", errors="ignore")

    text = text.strip()
    if not text:
        raise ValueError("Uploaded document did not contain extractable text.")
    return filename, text
