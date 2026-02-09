# PART 7. RAG 튜닝 및 이미지 처리 (고급)

## 7.1 성능 향상을 위한 처방법
- ReRanker: 1차 검색 결과를 Cross-Encoder로 재순위화하여 정확도 극대화
- Hybrid Search: BM25(키워드) + Vector Search 결합
- Advanced Retriever: Parent Document Retriever, Self-Query 등 활용

## 7.2 PDF 이미지 처리 (Vision 하이브리드)
- DeepSeek R1은 텍스트 전용이므로, 인덱싱 단계에서 Vision 모델(LLaVA)을 활용
- 하이브리드 로직:
  - 텍스트 위주 영역 → EasyOCR로 텍스트 추출
  - 차트/다이어그램 → LLaVA로 캡션 생성 후 텍스트화
- 검색 시:
  - 텍스트 청크와 함께 관련 이미지 경로를 메타데이터로 반환하여 UI에 표시
