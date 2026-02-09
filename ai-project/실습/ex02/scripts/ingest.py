from __future__ import annotations

import json
import sys
from pathlib import Path

from core.config import DOCS_DIR, PROCESSED_DIR
from core.utils import file_hash
from scripts.converter.base import convert_file


def ingest(source_dir: Path = DOCS_DIR, output_dir: Path = PROCESSED_DIR) -> list[Path]:
    # 변환 결과/메타데이터를 저장할 디렉터리 준비
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "manifest.jsonl"
    outputs: list[Path] = []

    # 문서 목록을 순회하며 변환 + manifest 기록
    with manifest_path.open("w", encoding="utf-8") as manifest:
        for path in sorted(source_dir.rglob("*")):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix not in {".pdf", ".docx", ".doc", ".png", ".jpg", ".jpeg", ".xlsx", ".xlsm", ".xltx", ".xltm"}:
                continue
            content_hash = file_hash(path)
            doc_id = f"{path.stem}_{content_hash[:8]}"
            text = convert_file(path)
            out_path = output_dir / f"{doc_id}.md"
            out_path.write_text(text, encoding="utf-8")
            outputs.append(out_path)

            # 문서 메타데이터를 JSONL로 누적 기록
            manifest.write(
                json.dumps(
                    {
                        "doc_id": doc_id,
                        "source_path": str(path),
                        "processed_path": str(out_path),
                        "hash": content_hash,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    return outputs


def main() -> int:
    outputs = ingest()
    print(f"ingested: {len(outputs)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
