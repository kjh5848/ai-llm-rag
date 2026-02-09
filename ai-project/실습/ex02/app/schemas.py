"""API 요청/응답 스키마 정의."""

from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel


class AskRequest(BaseModel):
    # 사용자 질문과 옵션(검색 개수/라우팅 강제)을 입력받는다.
    question: str
    top_k: int | None = None
    force_route: str | None = None
    category: str | None = None


class AskResponse(BaseModel):
    # LLM 답변과 라우팅 근거, 사용한 데이터 스냅샷을 반환한다.
    answer: str
    route: str
    reason: str
    structured_rows: list[dict]
    context_chunks: list[dict]


class EmployeeCreate(BaseModel):
    # 직원 등록 요청
    name: str
    dept: str
    email: str
    hire_date: date


class EmployeeUpdate(BaseModel):
    # 직원 수정 요청(부분 업데이트 허용)
    name: Optional[str] = None
    dept: Optional[str] = None
    email: Optional[str] = None
    hire_date: Optional[date] = None


class EmployeeOut(BaseModel):
    # 직원 응답
    id: int
    name: str
    dept: str
    email: str
    hire_date: date


class LeaveUsage(BaseModel):
    # 휴가 사용 등록 요청
    employee_id: int
    year: int
    days: float


class LeaveUpdate(BaseModel):
    # 휴가 데이터 강제 수정 요청
    employee_id: Optional[int] = None
    year: Optional[int] = None
    total: Optional[float] = None
    used: Optional[float] = None
    remaining: Optional[float] = None


class LeaveOut(BaseModel):
    # 휴가 응답
    id: int
    employee_id: int
    year: int
    total: float
    used: float
    remaining: float


class SalesCreate(BaseModel):
    # 매출 입력 요청
    dept: str
    amount: float
    date: date
    description: Optional[str] = None


class SalesOut(BaseModel):
    # 매출 응답
    id: int
    dept: str
    amount: float
    date: date
    description: Optional[str] = None


class SalesSummary(BaseModel):
    # 매출 집계 응답
    dept: str
    total_sales: float
