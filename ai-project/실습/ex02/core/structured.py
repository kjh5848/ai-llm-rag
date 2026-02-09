"""PostgreSQL 기반 정형 데이터 질의 모듈."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor

from core.config import DATABASE_URL


@dataclass
class StructuredResult:
    sql: str
    rows: list[dict[str, Any]]


def _connect():
    # PostgreSQL 연결 생성
    return psycopg2.connect(DATABASE_URL)


def query(sql: str, params: tuple[Any, ...] = (), fetch: bool = True) -> StructuredResult:
    # 공통 질의 실행 헬퍼 (RealDictCursor 사용)
    with _connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall() if fetch else []
        conn.commit()
    return StructuredResult(sql=sql, rows=list(rows))


def get_employee(employee_id: int) -> StructuredResult:
    # 직원 단건 조회
    return query("SELECT * FROM employees WHERE id = %s", (employee_id,))


def find_employee_by_name(name: str) -> StructuredResult:
    # 이름으로 직원 검색
    return query("SELECT * FROM employees WHERE name ILIKE %s", (f"%{name}%",))


def create_employee(name: str, dept: str, email: str, hire_date: str) -> StructuredResult:
    # 직원 등록
    return query(
        "INSERT INTO employees(name, dept, email, hire_date) VALUES (%s, %s, %s, %s) RETURNING *",
        (name, dept, email, hire_date),
    )


def update_employee(employee_id: int, fields: dict[str, Any]) -> StructuredResult:
    # 직원 정보 수정(가변 필드)
    if not fields:
        return get_employee(employee_id)
    set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
    params = tuple(fields.values()) + (employee_id,)
    return query(
        f"UPDATE employees SET {set_clause} WHERE id = %s RETURNING *",
        params,
    )


def delete_employee(employee_id: int) -> StructuredResult:
    # 직원 삭제
    return query("DELETE FROM employees WHERE id = %s RETURNING *", (employee_id,))


def get_vacation_balance(employee_id: int) -> StructuredResult:
    # 휴가 잔여량 조회
    return query(
        """
        SELECT lb.*
        FROM leave_balance lb
        WHERE lb.employee_id = %s
        ORDER BY lb.year DESC
        """,
        (employee_id,),
    )


def use_vacation(employee_id: int, year: int, days: float) -> StructuredResult:
    # 휴가 사용 처리 후 잔여량 반환
    with _connect() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE leave_balance
                SET used = used + %s,
                    remaining = remaining - %s
                WHERE employee_id = %s AND year = %s
                RETURNING *
                """,
                (days, days, employee_id, year),
            )
            rows = cur.fetchall()
        conn.commit()
    return StructuredResult(sql="use_vacation", rows=list(rows))


def update_leave(leave_id: int, fields: dict[str, Any]) -> StructuredResult:
    # 휴가 데이터 강제 수정
    if not fields:
        return query("SELECT * FROM leave_balance WHERE id = %s", (leave_id,))
    set_clause = ", ".join(f"{key} = %s" for key in fields.keys())
    params = tuple(fields.values()) + (leave_id,)
    return query(
        f"UPDATE leave_balance SET {set_clause} WHERE id = %s RETURNING *",
        params,
    )


def get_leaves_by_employee(employee_id: int) -> StructuredResult:
    # 직원별 휴가 목록
    return query("SELECT * FROM leave_balance WHERE employee_id = %s ORDER BY year DESC", (employee_id,))


def sales_by_department(start_date: str, end_date: str) -> StructuredResult:
    # 기간 내 부서별 매출 집계
    return query(
        """
        SELECT dept, SUM(amount) AS total_sales
        FROM sales
        WHERE date BETWEEN %s AND %s
        GROUP BY dept
        ORDER BY total_sales DESC
        """,
        (start_date, end_date),
    )


def sales_by_quarter(year: int, quarter: int) -> StructuredResult:
    # 분기 시작/종료일 계산 후 부서별 매출 집계 호출
    start_month = 1 + (quarter - 1) * 3
    end_month = start_month + 2
    start_date = f"{year}-{start_month:02d}-01"
    end_date = f"{year}-{end_month:02d}-31"
    return sales_by_department(start_date, end_date)


def create_sale(dept: str, amount: float, date: str, description: str | None) -> StructuredResult:
    # 매출 데이터 입력
    return query(
        "INSERT INTO sales(dept, amount, date, description) VALUES (%s, %s, %s, %s) RETURNING *",
        (dept, amount, date, description),
    )


def sales_period(start_date: str, end_date: str) -> StructuredResult:
    # 특정 기간 매출 조회
    return query(
        "SELECT * FROM sales WHERE date BETWEEN %s AND %s ORDER BY date ASC",
        (start_date, end_date),
    )


def sales_by_dept(dept: str, start_date: str | None = None, end_date: str | None = None) -> StructuredResult:
    # 부서별 매출 집계 결과 조회
    if start_date and end_date:
        return query(
            """
            SELECT dept, SUM(amount) AS total_sales
            FROM sales
            WHERE dept = %s AND date BETWEEN %s AND %s
            GROUP BY dept
            """,
            (dept, start_date, end_date),
        )
    return query(
        "SELECT dept, SUM(amount) AS total_sales FROM sales WHERE dept = %s GROUP BY dept",
        (dept,),
    )
