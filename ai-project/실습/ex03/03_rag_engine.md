# PART 4. RAG로 Q&A 엔진 만들기 (핵심 구현)

"일단 동작하는 RAG"를 구축하고 점진적으로 확장하는 단계입니다.

## 4.1 LangChain 기반 RAG 파이프라인
- 질문 입력: 사용자 질문 접수
- Retriever: 질문과 유사한 문서 청크를 VectorDB에서 검색
- Prompt 주입: 검색된 컨텍스트를 프롬프트 템플릿에 삽입
- LLM 생성: DeepSeek R1이 답변 생성

## 4.2 프롬프트 엔지니어링 전략
```
다음 문서를 참고하여 질문에 답하세요.
문서에 없는 내용은 '확인되지 않음'이라고 답하세요.
반드시 출처(문서명, 섹션)를 함께 제시하세요.

[문서]
{context}

[질문]
{question}
```

## 4.3 출력 포맷 및 UI 연결
- 구조화된 응답: `answer`와 참고한 `sources` 리스트를 함께 반환
- UI: FastAPI(Streaming Response) + JavaScript 대화형 UI
