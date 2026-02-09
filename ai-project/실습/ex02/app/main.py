"""FastAPI 진입점: 질문을 라우팅하고 정형/비정형 데이터를 조합해 답변을 생성한다."""

from __future__ import annotations

import re

from fastapi import FastAPI, HTTPException, Query

from app.schemas import (
    AskRequest,
    AskResponse,
    EmployeeCreate,
    EmployeeOut,
    EmployeeUpdate,
    LeaveOut,
    LeaveUpdate,
    LeaveUsage,
    SalesCreate,
    SalesOut,
    SalesSummary,
)
from core import rag as rag_module
from core import structured as structured_module
from core.config import DEFAULT_TOP_K
from core.llm import LLMError, generate
from core.prompts import render_template
from core.router import RouteDecision, classify_question

# API 서버와 로컬 RAG 엔진을 초기화한다.
app = FastAPI(title="Internal RAG + MCP Assistant")
# BM25/Chroma 중 설정값에 따라 검색을 선택한다.
rag_engine = rag_module.LocalRAG()


@app.get("/health")
def health() -> dict[str, str]:
    # 간단한 헬스체크 엔드포인트
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    # 1) 질문 유효성 확인
    question = req.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="question is required")

    # 2) 라우팅 결정(강제 라우팅이 있으면 우선)
    if req.force_route:
        decision = RouteDecision(req.force_route, "사용자 강제 지정")
    else:
        decision = classify_question(question)

    # 3) 검색 결과 개수 기본값 적용
    top_k = req.top_k or DEFAULT_TOP_K

    structured_rows: list[dict] = []
    context_chunks: list[dict] = []

    # 4) 정형 데이터 질의(간단한 키워드 기반 규칙)
    if decision.route in ("structured", "hybrid"):
        if any(k in question for k in ["매출", "부서"]):
            year_match = re.search(r"(20\\d{2})\\s*년", question)
            quarter_match = re.search(r"([1-4])\\s*분기|Q([1-4])", question, re.IGNORECASE)
            year = int(year_match.group(1)) if year_match else 2026
            quarter = int(quarter_match.group(1) or quarter_match.group(2)) if quarter_match else 4
            result = structured_module.sales_by_quarter(year, quarter)
        elif any(k in question for k in ["휴가", "잔여"]):
            emp_match = re.search(r"(\\d{4})", question)
            employee_id = int(emp_match.group(1)) if emp_match else 1001
            result = structured_module.get_vacation_balance(employee_id)
        else:
            result = structured_module.query("SELECT * FROM employees LIMIT 5")
        structured_rows = result.rows

    # 5) 비정형 문서 검색(RAG)
    if decision.route in ("unstructured", "hybrid"):
        # category가 있으면 Chroma 메타데이터 필터로 사용
        results = rag_module.retrieve(question, top_k=top_k, category=req.category)
        context_chunks = [
            {
                "doc_id": r.chunk.doc_id,
                "chunk_id": r.chunk.chunk_id,
                "score": r.score,
                "text": r.chunk.text,
            }
            for r in results
        ]

    # 6) 검색 결과를 프롬프트에 넣기 위한 컨텍스트 문자열로 변환
    context_text = ""
    if context_chunks:
        context_text = "\n\n".join(
            f"[doc:{chunk['doc_id']}#chunk{chunk['chunk_id']}]\n{chunk['text']}"
            for chunk in context_chunks
        )

    # 7) Jinja2 템플릿으로 최종 프롬프트 생성
    prompt = render_template(
        "answer_prompt.j2",
        question=question,
        structured_data=structured_rows,
        context=context_text,
    )

    # 8) LLM 호출(실패 시 디버깅을 위해 프롬프트 포함)
    try:
        answer = generate(prompt)
    except LLMError as exc:
        answer = f"[LLM_ERROR] {exc}\n\n{prompt}"

    # 9) 응답 페이로드 구성
    return AskResponse(
        answer=answer,
        route=decision.route,
        reason=decision.reason,
        structured_rows=structured_rows,
        context_chunks=context_chunks,
    )


# ---------------------------
# 직원 관리 API
# ---------------------------


@app.post("/employees", response_model=EmployeeOut)
def create_employee(req: EmployeeCreate) -> EmployeeOut:
    # 신규 직원 등록
    result = structured_module.create_employee(
        name=req.name,
        dept=req.dept,
        email=req.email,
        hire_date=str(req.hire_date),
    )
    if not result.rows:
        raise HTTPException(status_code=500, detail="employee create failed")
    return EmployeeOut(**result.rows[0])


@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int) -> EmployeeOut:
    # 직원 정보 조회
    result = structured_module.get_employee(employee_id)
    if not result.rows:
        raise HTTPException(status_code=404, detail="employee not found")
    return EmployeeOut(**result.rows[0])


@app.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, req: EmployeeUpdate) -> EmployeeOut:
    # 직원 정보 수정 (부분 업데이트)
    try:
        fields = req.model_dump(exclude_unset=True)
    except AttributeError:
        fields = req.dict(exclude_unset=True)
    result = structured_module.update_employee(employee_id, fields)
    if not result.rows:
        raise HTTPException(status_code=404, detail="employee not found")
    return EmployeeOut(**result.rows[0])


@app.delete("/employees/{employee_id}", response_model=EmployeeOut)
def delete_employee(employee_id: int) -> EmployeeOut:
    # 직원 삭제
    result = structured_module.delete_employee(employee_id)
    if not result.rows:
        raise HTTPException(status_code=404, detail="employee not found")
    return EmployeeOut(**result.rows[0])


# ---------------------------
# 휴가 관리 API
# ---------------------------


@app.get("/leaves/{employee_id}", response_model=list[LeaveOut])
def get_leaves(employee_id: int) -> list[LeaveOut]:
    # 직원별 휴가 잔여량 조회
    result = structured_module.get_leaves_by_employee(employee_id)
    return [LeaveOut(**row) for row in result.rows]


@app.post("/leaves/usage", response_model=LeaveOut)
def use_leave(req: LeaveUsage) -> LeaveOut:
    # 휴가 사용 등록 (잔여량 자동 차감)
    result = structured_module.use_vacation(req.employee_id, req.year, req.days)
    if not result.rows:
        raise HTTPException(status_code=404, detail="leave balance not found")
    return LeaveOut(**result.rows[0])


@app.put("/leaves/{leave_id}", response_model=LeaveOut)
def update_leave(leave_id: int, req: LeaveUpdate) -> LeaveOut:
    # 휴가 데이터 강제 수정 (관리자용)
    try:
        fields = req.model_dump(exclude_unset=True)
    except AttributeError:
        fields = req.dict(exclude_unset=True)
    result = structured_module.update_leave(leave_id, fields)
    if not result.rows:
        raise HTTPException(status_code=404, detail="leave not found")
    return LeaveOut(**result.rows[0])


# ---------------------------
# 매출 관리 API
# ---------------------------


@app.post("/sales", response_model=SalesOut)
def create_sale(req: SalesCreate) -> SalesOut:
    # 매출 데이터 입력
    result = structured_module.create_sale(
        dept=req.dept,
        amount=req.amount,
        date=str(req.date),
        description=req.description,
    )
    if not result.rows:
        raise HTTPException(status_code=500, detail="sales create failed")
    return SalesOut(**result.rows[0])


@app.get("/sales/period", response_model=list[SalesOut])
def get_sales_period(
    start: str = Query(..., description="시작일 (YYYY-MM-DD)"),
    end: str = Query(..., description="종료일 (YYYY-MM-DD)"),
) -> list[SalesOut]:
    # 특정 기간별 매출 조회
    result = structured_module.sales_period(start, end)
    return [SalesOut(**row) for row in result.rows]


@app.get("/sales/dept/{dept_name}", response_model=SalesSummary)
def get_sales_by_dept(
    dept_name: str,
    start: str | None = Query(None, description="시작일 (YYYY-MM-DD)"),
    end: str | None = Query(None, description="종료일 (YYYY-MM-DD)"),
) -> SalesSummary:
    # 부서별 매출 집계 결과 조회
    result = structured_module.sales_by_dept(dept_name, start, end)
    if not result.rows:
        raise HTTPException(status_code=404, detail="sales not found")
    row = result.rows[0]
    return SalesSummary(dept=row["dept"], total_sales=float(row["total_sales"]))
