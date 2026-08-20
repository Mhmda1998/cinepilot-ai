from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
}


def load_document(file_path: str) -> dict:
    """Load a supported document into plain text."""

    path = Path(file_path)

    if not path.exists():
        return {
            "success": False,
            "error": f"File not found: {file_path}",
        }

    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        return {
            "success": False,
            "error": f"Unsupported file type: {suffix}",
        }

    if suffix == ".pdf":
        return _load_pdf(path)

    text = path.read_text(encoding="utf-8")

    return {
        "success": True,
        "file_name": path.name,
        "file_type": suffix,
        "text": text,
        "characters": len(text),
    }


def _load_pdf(path: Path) -> dict:
    """Load text from a PDF document."""

    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        text = "\n\n".join(pages)

        return {
            "success": True,
            "file_name": path.name,
            "file_type": ".pdf",
            "text": text,
            "pages": len(reader.pages),
            "characters": len(text),
        }

    except ImportError:
        return {
            "success": False,
            "error": "pypdf is not installed.",
        }
