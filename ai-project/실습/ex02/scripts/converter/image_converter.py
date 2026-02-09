"""이미지(OCR) -> 텍스트 변환."""

from __future__ import annotations

from pathlib import Path


def convert_image(path: Path) -> str:
    try:
        from PIL import Image
        import pytesseract
    except ImportError as exc:
        raise RuntimeError("pillow + pytesseract가 필요합니다. requirements-optional.txt 참고") from exc
    image = Image.open(path)
    return pytesseract.image_to_string(image, lang="kor+eng").strip()
