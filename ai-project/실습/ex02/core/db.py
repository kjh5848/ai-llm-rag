"""PostgreSQL 연결 및 스키마/시드 유틸."""

from __future__ import annotations

from typing import Iterable

import psycopg2
from psycopg2.extensions import connection as PgConnection

from core.config import DATABASE_URL


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    dept TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    hire_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS leave_balance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    year INTEGER NOT NULL,
    total REAL NOT NULL,
    used REAL NOT NULL,
    remaining REAL NOT NULL,
    UNIQUE(employee_id, year)
);

CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    dept TEXT NOT NULL,
    amount NUMERIC NOT NULL,
    date DATE NOT NULL,
    description TEXT
);
"""


SEED_EMPLOYEES = [
    ("김주혁", "개발", "juhyeok@company.com", "2022-03-01"),
    ("이서연", "인사", "seoyeon@company.com", "2021-07-15"),
    ("박민수", "영업", "minsu@company.com", "2020-11-20"),
    ("정하늘", "보안", "haneul@company.com", "2023-01-10"),
]

SEED_LEAVES = [
    # employee_id는 시드 입력 순서에 맞춰 1~4로 가정
    (1, 2026, 15.0, 3.0, 12.0),
    (2, 2026, 15.0, 6.5, 8.5),
    (3, 2026, 15.0, 10.0, 5.0),
    (4, 2026, 15.0, 5.0, 10.0),
]

SEED_SALES = [
    ("영업", 12000000, "2026-10-05", "Q4 신규 계약"),
    ("영업", 18000000, "2026-11-12", "리뉴얼 매출"),
    ("마케팅", 5200000, "2026-10-22", "캠페인 집행"),
    ("마케팅", 6100000, "2026-12-03", "성과형 광고"),
    ("개발", 3000000, "2026-12-18", "내부 프로젝트"),
]


def connect() -> PgConnection:
    """PostgreSQL 연결을 생성한다."""
    return psycopg2.connect(DATABASE_URL)


def init_db() -> None:
    """스키마를 생성한다."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(SCHEMA_SQL)
        conn.commit()


def seed_db() -> None:
    """샘플 데이터를 삽입한다."""
    init_db()
    with connect() as conn:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO employees(name, dept, email, hire_date) VALUES (%s, %s, %s, %s) ON CONFLICT (email) DO NOTHING",
                SEED_EMPLOYEES,
            )
            # employee_id 매핑을 위해 현재 employees id 조회
            cur.execute("SELECT id, email FROM employees ORDER BY id")
            id_map = {row[1]: row[0] for row in cur.fetchall()}

            resolved_leaves: list[tuple[int, int, float, float, float]] = []
            for idx, leave in enumerate(SEED_LEAVES):
                employee_email = SEED_EMPLOYEES[idx][2]
                employee_id = id_map.get(employee_email)
                if employee_id is None:
                    continue
                resolved_leaves.append((employee_id, *leave[1:]))

            cur.executemany(
                "INSERT INTO leave_balance(employee_id, year, total, used, remaining) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (employee_id, year) DO NOTHING",
                resolved_leaves,
            )
            cur.executemany(
                "INSERT INTO sales(dept, amount, date, description) VALUES (%s, %s, %s, %s)",
                SEED_SALES,
            )
        conn.commit()
