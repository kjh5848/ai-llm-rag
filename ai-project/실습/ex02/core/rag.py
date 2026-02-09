"""BM25 또는 Chroma 기반 로컬 RAG 검색기."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from core.config import DEFAULT_TOP_K, PROCESSED_DIR, RAG_BACKEND
from core.utils import DocumentChunk, chunk_text, tokenize
from core.vectordb import search as chroma_search


@dataclass
class RetrievalResult:
    chunk: DocumentChunk
    score: float


class BM25Index:
    # 문서 집합을 인덱싱하고 질의에 대해 BM25 점수를 계산한다.
    def __init__(self, k1: float = 1.2, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.documents: List[DocumentChunk] = []
        self.doc_tokens: List[List[str]] = []
        self.doc_freq: dict[str, int] = {}
        self.avgdl = 0.0

    def add_documents(self, docs: Iterable[DocumentChunk]) -> None:
        # 문서를 토큰화해 인덱스에 적재
        for doc in docs:
            tokens = tokenize(doc.text)
            self.documents.append(doc)
            self.doc_tokens.append(tokens)
            seen = set(tokens)
            for t in seen:
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1
        total_len = sum(len(toks) for toks in self.doc_tokens)
        self.avgdl = total_len / max(1, len(self.doc_tokens))

    def _idf(self, term: str) -> float:
        # 문서 빈도 기반 IDF 계산
        n_docs = len(self.doc_tokens)
        df = self.doc_freq.get(term, 0)
        return max(0.0, ((n_docs - df + 0.5) / (df + 0.5)))

    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> List[RetrievalResult]:
        # 질의 토큰을 기준으로 각 문서의 BM25 점수 산출
        q_tokens = tokenize(query)
        if not q_tokens:
            return []
        scores: List[float] = []
        for tokens in self.doc_tokens:
            score = 0.0
            doc_len = len(tokens)
            freqs: dict[str, int] = {}
            for t in tokens:
                freqs[t] = freqs.get(t, 0) + 1
            for term in q_tokens:
                if term not in freqs:
                    continue
                tf = freqs[term]
                idf = self._idf(term)
                denom = tf + self.k1 * (1 - self.b + self.b * doc_len / max(1, self.avgdl))
                score += idf * (tf * (self.k1 + 1) / denom)
            scores.append(score)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        results: List[RetrievalResult] = []
        for idx, score in ranked:
            if score <= 0:
                continue
            results.append(RetrievalResult(self.documents[idx], score))
        return results


class LocalRAG:
    # 변환된 Markdown 문서를 로컬에서 로딩해 BM25로 검색한다.
    def __init__(self, processed_dir: Path | None = None) -> None:
        self.processed_dir = processed_dir or PROCESSED_DIR
        self.index = BM25Index()
        self._loaded = False

    def load(self) -> None:
        # 한 번만 문서를 로드하여 인덱스 구성
        if self._loaded:
            return
        docs: List[DocumentChunk] = []
        for path in sorted(self.processed_dir.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            for i, chunk in enumerate(chunk_text(text)):
                docs.append(DocumentChunk(
                    doc_id=path.stem,
                    source_path=str(path),
                    chunk_id=i,
                    text=chunk,
                ))
        self.index.add_documents(docs)
        self._loaded = True

    def retrieve(self, question: str, top_k: int = DEFAULT_TOP_K) -> List[RetrievalResult]:
        # 질문을 인덱싱된 문서와 매칭해 상위 K개를 반환
        self.load()
        return self.index.search(question, top_k=top_k)


def format_context(results: List[RetrievalResult]) -> str:
    # LLM 프롬프트에 넣을 컨텍스트 문자열로 포맷팅
    if not results:
        return ""
    lines = []
    for res in results:
        lines.append(f"[doc:{res.chunk.doc_id}#chunk{res.chunk.chunk_id}]\n{res.chunk.text}")
    return "\n\n".join(lines)


def retrieve(question: str, top_k: int = DEFAULT_TOP_K, category: str | None = None) -> List[RetrievalResult]:
    # 환경 변수로 RAG 백엔드를 선택
    if RAG_BACKEND == "chroma":
        vec_results = chroma_search(question, top_k=top_k, category=category)
        return [RetrievalResult(chunk=r.chunk, score=r.score) for r in vec_results]
    # 기본값은 BM25
    rag = LocalRAG()
    return rag.retrieve(question, top_k=top_k)
