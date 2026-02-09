"""질문을 정형/비정형/하이브리드로 분류하는 간단한 라우터."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Route = Literal["structured", "unstructured", "hybrid"]


# 정형(DB) 질의를 유도하는 키워드
STRUCTURED_HINTS = [
    "매출",
    "잔여",
    "휴가",
    "근태",
    "직원",
    "부서",
    "정원",
    "인원",
    "연봉",
    "급여",
    "목록",
    "조회",
    "기간",
    "집계",
    "합계",
    "평균",
    "통계",
]

# 비정형(문서) 질의를 유도하는 키워드
UNSTRUCTURED_HINTS = [
    "규정",
    "정책",
    "가이드",
    "매뉴얼",
    "절차",
    "보안",
    "온보딩",
    "FAQ",
    "지침",
    "설명",
    "문서",
]


@dataclass
class RouteDecision:
    route: Route
    reason: str


def classify_question(question: str) -> RouteDecision:
    # 키워드 존재 여부로 라우팅 경로를 결정
    q = question.strip().lower()
    structured = any(h in q for h in STRUCTURED_HINTS)
    unstructured = any(h in q for h in UNSTRUCTURED_HINTS)

    if structured and unstructured:
        return RouteDecision("hybrid", "정형/비정형 단서가 모두 존재")
    if structured:
        return RouteDecision("structured", "정형 데이터 키워드 감지")
    if unstructured:
        return RouteDecision("unstructured", "비정형 문서 키워드 감지")
    return RouteDecision("hybrid", "단서 부족: 하이브리드로 처리")
