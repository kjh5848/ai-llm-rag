import sys
import os
from typing import Optional, List

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from mcp.server.fastmcp import FastMCP
from db import get_db_connection
import crud

# MCP 서버 인스턴스 생성
app = FastMCP("Metacoding Assistant")

# 도구 등록: 직원 관리
@app.tool()
def create_employee(name: str, dept: str, email: str, hire_date: str):
    """신규 직원을 등록합니다."""
    conn = get_db_connection()
    try:
        return crud.create_employee(conn, name, dept, email, hire_date)
    finally:
        conn.close()

@app.tool()
def get_employee(employee_id: int):
    """특정 직원 정보를 조회합니다."""
    conn = get_db_connection()
    try:
        employee = crud.get_employee(conn, employee_id)
        return employee if employee else "Employee not found"
    finally:
        conn.close()

@app.tool()
def update_employee(employee_id: int, name: Optional[str] = None, dept: Optional[str] = None, email: Optional[str] = None, hire_date: Optional[str] = None):
    """직원 정보를 수정합니다."""
    conn = get_db_connection()
    try:
        updated = crud.update_employee(conn, employee_id, name, dept, email, hire_date)
        return updated if updated else "Employee not found"
    finally:
        conn.close()

@app.tool()
def delete_employee(employee_id: int):
    """직원을 삭제합니다."""
    conn = get_db_connection()
    try:
        ok = crud.delete_employee(conn, employee_id)
        return {"deleted": ok}
    finally:
        conn.close()

# 도구 등록: 휴가 관리
@app.tool()
def get_leave_balance(employee_id: int):
    """특정 직원의 잔여 휴가를 조회합니다."""
    conn = get_db_connection()
    try:
        leave = crud.get_leave_by_employee(conn, employee_id)
        return leave if leave else "Leave record not found"
    finally:
        conn.close()

@app.tool()
def use_leave(employee_id: int, days: float):
    """휴가 사용을 등록하고 잔여량을 자동 차감합니다."""
    conn = get_db_connection()
    try:
        updated = crud.use_leave(conn, employee_id, days)
        return updated if updated else "Leave record not found or error occurred"
    finally:
        conn.close()

@app.tool()
def update_leave(leave_id: int, employee_id: Optional[int] = None, year: Optional[int] = None, total: Optional[float] = None, used: Optional[float] = None, remaining: Optional[float] = None):
    """휴가 데이터를 강제로 수정합니다 (관리자용)."""
    conn = get_db_connection()
    try:
        updated = crud.update_leave(conn, leave_id, employee_id, year, total, used, remaining)
        return updated if updated else "Leave record not found"
    finally:
        conn.close()

# 도구 등록: 매출 관리
@app.tool()
def create_sale(dept: str, amount: int, date: str, description: Optional[str] = None):
    """매출 데이터를 입력합니다."""
    conn = get_db_connection()
    try:
        return crud.create_sale(conn, dept, amount, date, description)
    finally:
        conn.close()

@app.tool()
def get_sales_period(start_date: str, end_date: str):
    """특정 기간별 매출을 조회합니다. 날짜 형식: YYYY-MM-DD"""
    conn = get_db_connection()
    try:
        return crud.get_sales_period(conn, start_date, end_date)
    finally:
        conn.close()

@app.tool()
def get_sales_by_dept(dept_name: str):
    """부서별 매출 집계 결과를 조회합니다."""
    conn = get_db_connection()
    try:
        return crud.get_sales_by_dept(conn, dept_name)
    finally:
        conn.close()

if __name__ == "__main__":
    app.run()
