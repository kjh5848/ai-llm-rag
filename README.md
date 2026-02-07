# AI 업무 비서(RAG + MCP) 구축 프로젝트

이 저장소는 **'사내 문서 기반 AI 업무 비서'** 집필 및 실습을 위한 전체 코드를 담고 있습니다.

## 📂 프로젝트 구조

### 📝 원고 (Manuscript)

- `00_manuscript/`: 각 장별(1장~10장) 도서 본문 원고 및 시각 자료.

### 📚 가이드 및 참조 (Reference)

- `01_reference/`: 기술 상세 레퍼런스 가이드북 및 관련 PDF 문서.

### 💻 실습 코드 (Hands-on)

각 챕터의 단계별 실습 코드는 아래 폴더에 구성되어 있습니다.

- `02_basic_rag/`: 2장 기초 RAG 실습 (LLM 한계 테스트 및 검색 엔진 기초).
- `03_setup/`: 3장 환경 설정 (Docker, DB 세팅).
- `04_base_system/`: 4장 베이스 시스템 (가상 사내 관리 대시보드 및 FastAPI 엔드포인트).
- `06_vectordb/`: 6장 지식 수치화 (ChromaDB 연동).
- `07_rag_engine/`: 7장 Q&A 엔진 구현.
- `08_agent/`: 8장 지능형 에이전트 설계.
- `09_ui/`: 9장 최종 UI 연동.
- `10_tuning/`: 10장 시스템 튜닝 (Hybrid 검색 및 ReRanker).

---

## 🚀 시작하기

1. **환경 설정**: `03_setup` 폴더의 안내에 따라 Docker 및 가상환경을 구축하십시오.
2. **실습**: 2장부터 순서대로 실습 코드를 실행하며 학습하십시오.
3. **참조**: 기술적 배경이 궁금할 때는 `01_reference`의 가이드북을 확인하십시오.

---

## 🛠 기술 스택

- **Model**: DeepSeek-R1 (Ollama), LLaVA
- **Orchestration**: LangChain, Model Context Protocol (MCP)
- **Backend**: FastAPI
- **Database**: PostgreSQL (정형), ChromaDB (벡터)
