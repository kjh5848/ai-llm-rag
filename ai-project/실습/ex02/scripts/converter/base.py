"""공통 변환 인터페이스 및 라우팅."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from core.config import DOCS_DIR, PROCESSED_DIR
from scripts.converter.docx_converter import convert_docx
from scripts.converter.image_converter import convert_image
from scripts.converter.pdf_converter import convert_pdf
from scripts.converter.xlsx_converter import convert_xlsx


_CONVERTERS: dict[str, Callable[[Path], str]] = {
    ".pdf": convert_pdf,
    ".docx": convert_docx,
    ".doc": convert_docx,
    ".png": convert_image,
    ".jpg": convert_image,
    ".jpeg": convert_image,
    ".xlsx": convert_xlsx,
    ".xlsm": convert_xlsx,
    ".xltx": convert_xlsx,
    ".xltm": convert_xlsx,
}


def convert_file(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in _CONVERTERS:
        raise ValueError(f"지원하지 않는 파일 형식: {suffix}")
    return _CONVERTERS[suffix](path)


def convert_dir(source_dir: Path = DOCS_DIR, output_dir: Path = PROCESSED_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for path in sorted(source_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in _CONVERTERS:
            continue
        text = convert_file(path)
        out_path = output_dir / f"{path.stem}.md"
        out_path.write_text(text, encoding="utf-8")
        outputs.append(out_path)
    return outputs
