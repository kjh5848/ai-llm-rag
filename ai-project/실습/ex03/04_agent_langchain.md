# PART 5 ~ 6. 통합 에이전트 및 LangChain 연결 전략

## 5.1 통합 에이전트(Router) 설계
- 사용자의 질문을 분석하여 적절한 도구를 선택
- 규칙/스키마 기반: 키워드("매출", "잔여") 매칭 시 MCP 호출
- LLM 판단: 복잡한 질문의 경우 LLM이 직접 도구 선택

## 6.1 LangChain 연결 3종 세트
- Router / Agent: 전체 오케스트레이션 및 도구 결정
- RAG Chain: 비정형 문서 검색 및 답변 생성 담당
- MCP Tools: SQL DB 조회를 위한 실질적인 함수(Tool) 집합

## 6.2 MCP Tool 상세 설계 (Python 예시)
- `@tool get_leave_balance`: 직원의 휴가 잔여일 조회
- `@tool get_sales_sum`: 부서별/기간별 매출 합계 계산
- `@tool search_documents`: VectorDB 기반 문서 검색 도구
