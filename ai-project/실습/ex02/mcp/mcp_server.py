"""FastMCP 기반 정형 데이터 도구 서버."""

from __future__ import annotations

from core import structured as structured_module
from mcp.db import seed_db

try:
    from fastmcp import FastMCP
except ImportError as exc:
    raise SystemExit("fastmcp가 설치되어 있지 않습니다. requirements-optional.txt 참고") from exc


# MCP 서버 인스턴스 생성
mcp = FastMCP("internal-db")


@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """직원 정보를 조회합니다."""
    # 내부 DB 질의 결과를 MCP 도구 응답 형태로 반환
    result = structured_module.get_employee(employee_id)
    return {"rows": result.rows}


@mcp.tool()
def find_employee_by_name(name: str) -> dict:
    """이름으로 직원을 검색합니다."""
    # 이름 부분일치 검색
    result = structured_module.find_employee_by_name(name)
    return {"rows": result.rows}


@mcp.tool()
def get_vacation_balance(employee_id: int) -> dict:
    """직원의 휴가 잔여량을 조회합니다."""
    # 휴가 잔여량 조회
    result = structured_module.get_vacation_balance(employee_id)
    return {"rows": result.rows}


@mcp.tool()
def use_vacation(employee_id: int, days: float) -> dict:
    """휴가를 사용 처리합니다."""
    # 휴가 차감 처리
    result = structured_module.use_vacation(employee_id, days)
    return {"rows": result.rows}


@mcp.tool()
def sales_by_quarter(year: int, quarter: int) -> dict:
    """분기별 부서 매출을 조회합니다."""
    # 분기 매출 집계
    result = structured_module.sales_by_quarter(year, quarter)
    return {"rows": result.rows}


if __name__ == "__main__":
    # 로컬 실행 시 샘플 데이터로 DB를 채운 뒤 서버 시작
    seed_db()
    mcp.run()
