"""텍스트 처리 및 문서 청킹 유틸리티."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


# 한글/영문/숫자 기준의 간단한 토큰 분리 규칙
TOKEN_RE = re.compile(r"[A-Za-z0-9가-힣_]+", re.UNICODE)


def tokenize(text: str) -> List[str]:
    # 텍스트를 소문자 토큰 리스트로 변환
    return [t.lower() for t in TOKEN_RE.findall(text)]


def chunk_text(text: str, max_chars: int = 900, overlap: int = 120) -> List[str]:
    # 문서를 문단 기준으로 자르고, 겹침(overlap)을 둔다.
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: List[str] = []
    current: List[str] = []
    length = 0

    def flush():
        # 현재 버퍼를 청크로 저장하고 overlap만큼 꼬리를 남긴다.
        nonlocal current, length
        if current:
            chunks.append("\n\n".join(current).strip())
            if overlap > 0:
                tail = "\n\n".join(current)[-overlap:]
                current = [tail] if tail else []
                length = len(tail)
            else:
                current = []
                length = 0

    for para in paragraphs:
        if length + len(para) + 2 > max_chars:
            flush()
        current.append(para)
        length += len(para) + 2
    flush()
    return [c for c in chunks if c]


def file_hash(path: Path) -> str:
    # 파일 해시를 계산해 문서 ID 생성에 사용
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


@dataclass
class DocumentChunk:
    # 문서 조각(청크) 메타데이터
    doc_id: str
    source_path: str
    chunk_id: int
    text: str
