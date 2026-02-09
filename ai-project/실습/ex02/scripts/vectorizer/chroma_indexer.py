"""Chroma VectorDB 인덱싱."""

from __future__ import annotations

import json
from pathlib import Path

from core.config import PROCESSED_DIR
from core.vectordb import index_documents


def index_processed(processed_dir: Path = PROCESSED_DIR) -> int:
    processed_files = sorted(Path(processed_dir).glob("*.md"))
    if not processed_files:
        return 0

    meta_map: dict[str, dict] = {}
    manifest_path = Path(processed_dir) / "manifest.jsonl"
    if manifest_path.exists():
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            doc_id = item.get("doc_id")
            if not doc_id:
                continue
            meta_map[doc_id] = {
                "source_path": item.get("source_path"),
            }

    return index_documents(processed_files, doc_meta_map=meta_map)
