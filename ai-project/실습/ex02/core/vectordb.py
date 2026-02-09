"""ChromaDB 기반 벡터 인덱스/검색."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import chromadb

from core.config import CHROMA_DIR, CHROMA_COLLECTION, EMBEDDING_MODEL, DEFAULT_TOP_K
from core.embeddings import embed_texts
from core.utils import DocumentChunk, chunk_text


@dataclass
class VectorResult:
    chunk: DocumentChunk
    score: float


def _client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _collection() -> chromadb.Collection:
    client = _client()
    return client.get_or_create_collection(name=CHROMA_COLLECTION)


def _infer_category(source_path: str | None) -> str | None:
    # source_path가 docs/<category>/... 형태면 카테고리를 추출
    if not source_path:
        return None
    parts = Path(source_path).parts
    if "docs" in parts:
        idx = parts.index("docs")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return None


def index_documents(
    processed_files: Iterable[Path],
    doc_meta_map: dict[str, dict] | None = None,
) -> int:
    # Markdown 문서를 청킹 후 Chroma에 저장
    col = _collection()
    total = 0
    for path in processed_files:
        text = path.read_text(encoding="utf-8")
        chunks = [c for c in chunk_text(text) if c.strip()]
        if not chunks:
            continue
        meta = (doc_meta_map or {}).get(path.stem, {})
        category = meta.get("category") or _infer_category(meta.get("source_path"))
        embeddings = embed_texts(chunks, EMBEDDING_MODEL)
        ids = [f"{path.stem}_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "doc_id": path.stem,
                "chunk_id": i,
                "source_path": str(path),
                "category": category,
            }
            for i in range(len(chunks))
        ]
        col.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
        total += len(chunks)
    return total


def search(query: str, top_k: int = DEFAULT_TOP_K, category: str | None = None) -> List[VectorResult]:
    # 쿼리를 임베딩해 상위 K개 문서를 검색
    col = _collection()
    q_emb = embed_texts([query], EMBEDDING_MODEL)[0]
    where = {"category": category} if category else None
    result = col.query(
        query_embeddings=[q_emb],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
        where=where,
    )
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    dists = result.get("distances", [[]])[0]

    outputs: List[VectorResult] = []
    for doc_text, meta, dist in zip(docs, metas, dists):
        chunk = DocumentChunk(
            doc_id=str(meta.get("doc_id")),
            source_path=str(meta.get("source_path")),
            chunk_id=int(meta.get("chunk_id")),
            text=doc_text,
        )
        # Chroma 거리값이 작을수록 유사 (score는 보기 좋게 역수 변환)
        score = 1.0 / (1.0 + float(dist))
        outputs.append(VectorResult(chunk=chunk, score=score))
    return outputs
