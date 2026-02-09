from typing import Dict, Any
from .llm_service import llm_service
from .vector_service import vector_service
from .db_service import db_service

class QAService:
    """
    하이브리드 Q&A 오케스트레이터 서비스.
    개별 전문 서비스(LLM, Vector, DB)를 조합하여 통합 검색 및 답변을 제공합니다.
    """
    def __init__(self):
        print("[QAService] Orchestrator Initialized.")

    def hybrid_search(self, query: str) -> Dict[str, Any]:
        """지능형 라우팅을 적용한 하이브리드 검색"""
        # 1. 질문 의도 분석 (Router 호출)
        analysis = llm_service.classify_intent(query)
        route = analysis.get("route", "hybrid")
        print(f"[QAService] Route determined: {route} (Reason: {analysis.get('reason')})")
        
        unstructured = []
        structured = {"employees": [], "sales": [], "leaves": []}
        
        # 2. 분석된 경로에 따라 선택적 검색 수행
        if route in ["unstructured", "hybrid"]:
            unstructured = vector_service.search_unstructured(query)
            
        if route in ["structured", "hybrid"]:
            structured = db_service.search_structured(query)
        
        return {
            "query": query,
            "unstructured": unstructured,
            "structured": structured,
            "route": route
        }

    def get_ai_answer(self, query: str, search_results: Dict[str, Any]) -> str:
        """검색 결과를 바탕으로 AI 답변 생성 및 컨텍스트 구성"""
        
        # 1. 컨텍스트 구성
        context_parts = []
        
        # 비정형 데이터 추가
        if search_results["unstructured"]:
            context_parts.append("[사내 문서 내용]")
            for doc in search_results["unstructured"]:
                context_parts.append(f"- {doc['content']} (출처: {doc['source']})")
        
        # 정형 데이터 추가
        structured = search_results["structured"]
        if structured["employees"] or structured["sales"] or structured["leaves"]:
            context_parts.append("\n[시스템 데이터베이스 정보]")
            if structured["employees"]:
                context_parts.append("- 직원: " + ", ".join([f"{e['name']}({e['dept']})" for e in structured["employees"]]))
            if structured["leaves"]:
                context_parts.append("- 휴가 잔여: " + ", ".join([f"{l['employee_name']}: {l['remaining']}일" for l in structured["leaves"]]))
            if structured["sales"]:
                context_parts.append(f"- 관련 매출 데이터 {len(structured['sales'])}건 존재")

        context_text = "\n".join(context_parts)
        
        # 2. 템플릿 기반 답변 생성 호출
        return llm_service.generate_answer(query, context_text)

# 싱글톤 인스턴스
qa_service = QAService()
