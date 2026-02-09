"""문서 임베딩 생성 유틸 (SentenceTransformers)."""

from __future__ import annotations

from functools import lru_cache
from typing import Iterable, List

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _load_model(model_name: str) -> SentenceTransformer:
    # 모델은 한 번만 로드하여 재사용
    return SentenceTransformer(model_name)


def embed_texts(texts: Iterable[str], model_name: str) -> List[list[float]]:
    # 텍스트 목록을 벡터로 변환
    model = _load_model(model_name)
    embeddings = model.encode(list(texts), show_progress_bar=False)
    return embeddings.tolist()
