"""DOCX -> 텍스트 변환."""

from __future__ import annotations

from pathlib import Path


def convert_docx(path: Path) -> str:
    try:
        import docx
    except ImportError as exc:
        raise RuntimeError("python-docx가 필요합니다. requirements-optional.txt 참고") from exc
    doc = docx.Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip()).strip()
