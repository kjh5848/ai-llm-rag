# PART 8. 운영 및 배포

## 아키텍처
- Nginx(Proxy) → FastAPI(Uvicorn) → LangChain Agent → Ollama(DeepSeek/LLaVA)

## 환경 구성
- Docker Compose를 활용한 서비스 격리

## 보안
- Prompt Injection 방지
- JWT 인증
- 민감 정보 마스킹 적용

## 기술 스택 요약 (메모리 16GB 기준)
- LLM: Ollama (DeepSeek R1 - 런타임용 / LLaVA - 인덱싱용)
- Backend: FastAPI, SQLAlchemy
- DB: PostgreSQL (정형), Chroma (벡터)
- Orchestration: LangChain, MCP
