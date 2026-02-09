"""환경 변수 기반 설정 모음."""

from __future__ import annotations

import os
from pathlib import Path

# 프로젝트 루트 기준 경로
BASE_DIR = Path(__file__).resolve().parents[1]

# 문서/데이터 경로 (환경 변수로 덮어쓸 수 있음)
DOCS_DIR = Path(os.getenv("DOCS_DIR", BASE_DIR / "docs"))
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))

# 파생 데이터 경로
PROCESSED_DIR = Path(os.getenv("PROCESSED_DIR", DATA_DIR / "processed"))
EMBEDDINGS_DIR = Path(os.getenv("EMBEDDINGS_DIR", DATA_DIR / "embeddings"))
QA_DIR = Path(os.getenv("QA_DIR", DATA_DIR / "qa"))
TEMPLATES_DIR = Path(os.getenv("TEMPLATES_DIR", BASE_DIR / "templates"))

# VectorDB 설정
CHROMA_DIR = Path(os.getenv("CHROMA_DIR", DATA_DIR / "chroma"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "company_docs")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "jhgan/ko-sroberta-multitask")
RAG_BACKEND = os.getenv("RAG_BACKEND", "bm25")  # bm25 | chroma

# 정형 데이터 저장소 (PostgreSQL)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_USER = os.getenv("DB_USER", "metacoding")
DB_PASSWORD = os.getenv("DB_PASSWORD", "metacoding1234")
DB_NAME = os.getenv("DB_NAME", "metacoding_db")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
)

# LLM 연결 정보
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))

# RAG 기본 검색 개수
DEFAULT_TOP_K = int(os.getenv("RAG_TOP_K", "4"))
