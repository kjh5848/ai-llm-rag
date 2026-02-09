"""docs/ 폴더의 원본 문서를 Markdown 텍스트로 변환한다."""

from __future__ import annotations

import sys
from pathlib import Path

from core.config import DOCS_DIR, PROCESSED_DIR
from scripts.converter.base import convert_dir


def main() -> int:
    outputs = convert_dir(DOCS_DIR, PROCESSED_DIR)
    print(f"converted: {len(outputs)} files")
    for out in outputs:
        print(f"- {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
