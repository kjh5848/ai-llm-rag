"""PDF -> 텍스트 변환."""

from __future__ import annotations

from pathlib import Path


def convert_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf가 필요합니다. requirements-indexing.txt 참고") from exc
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text)
    return "\n\n".join(pages).strip()
