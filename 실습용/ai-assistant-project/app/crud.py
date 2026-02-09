from typing import List, Optional, Dict, Any
import sqlite3


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return dict(row) if row is not None else {}


def list_employees(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute("SELECT * FROM employees ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def get_employee(conn: sqlite3.Connection, employee_id: int) -> Optional[Dict[str, Any]]:
    row = conn.execute("SELECT * FROM employees WHERE id = ?", (employee_id,)).fetchone()
    return _row_to_dict(row) if row else None


def create_employee(conn: sqlite3.Connection, name: str, dept: str, email: str, hire_date: str) -> Dict[str, Any]:
    cursor = conn.execute(
        "INSERT INTO employees (name, dept, email, hire_date) VALUES (?, ?, ?, ?)",
        (name, dept, email, hire_date),
    )
    conn.commit()
    return get_employee(conn, cursor.lastrowid)


def update_employee(
    conn: sqlite3.Connection,
    employee_id: int,
    name: Optional[str] = None,
    dept: Optional[str] = None,
    email: Optional[str] = None,
    hire_date: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    current = get_employee(conn, employee_id)
    if not current:
        return None
    name = name if name is not None else current["name"]
    dept = dept if dept is not None else current["dept"]
    email = email if email is not None else current["email"]
    hire_date = hire_date if hire_date is not None else current["hire_date"]
    conn.execute(
        "UPDATE employees SET name = ?, dept = ?, email = ?, hire_date = ? WHERE id = ?",
        (name, dept, email, hire_date, employee_id),
    )
    conn.commit()
    return get_employee(conn, employee_id)


def delete_employee(conn: sqlite3.Connection, employee_id: int) -> bool:
    cursor = conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
    conn.commit()
    return cursor.rowcount > 0


def list_leaves(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT l.*, e.name
        FROM leave_balance l
        JOIN employees e ON l.employee_id = e.id
        ORDER BY l.id DESC
        """
    ).fetchall()
    return [dict(row) for row in rows]


def get_leave_by_employee(conn: sqlite3.Connection, employee_id: int) -> Optional[Dict[str, Any]]:
    row = conn.execute(
        "SELECT * FROM leave_balance WHERE employee_id = ?",
        (employee_id,),
    ).fetchone()
    return _row_to_dict(row) if row else None


def get_leave_by_id(conn: sqlite3.Connection, leave_id: int) -> Optional[Dict[str, Any]]:
    row = conn.execute("SELECT * FROM leave_balance WHERE id = ?", (leave_id,)).fetchone()
    return _row_to_dict(row) if row else None


def use_leave(conn: sqlite3.Connection, employee_id: int, days: float) -> Optional[Dict[str, Any]]:
    leave = get_leave_by_employee(conn, employee_id)
    if not leave:
        return None
    new_used = float(leave["used"]) + float(days)
    new_remaining = float(leave["total"]) - new_used
    conn.execute(
        "UPDATE leave_balance SET used = ?, remaining = ? WHERE employee_id = ?",
        (new_used, new_remaining, employee_id),
    )
    conn.commit()
    return get_leave_by_employee(conn, employee_id)


def update_leave(
    conn: sqlite3.Connection,
    leave_id: int,
    employee_id: Optional[int] = None,
    year: Optional[int] = None,
    total: Optional[float] = None,
    used: Optional[float] = None,
    remaining: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    current = get_leave_by_id(conn, leave_id)
    if not current:
        return None
    employee_id = employee_id if employee_id is not None else current["employee_id"]
    year = year if year is not None else current["year"]
    total = total if total is not None else current["total"]
    used = used if used is not None else current["used"]
    remaining = remaining if remaining is not None else current["remaining"]
    conn.execute(
        """
        UPDATE leave_balance
        SET employee_id = ?, year = ?, total = ?, used = ?, remaining = ?
        WHERE id = ?
        """,
        (employee_id, year, total, used, remaining, leave_id),
    )
    conn.commit()
    return get_leave_by_id(conn, leave_id)


def list_sales(conn: sqlite3.Connection, limit: int = 50) -> List[Dict[str, Any]]:
    rows = conn.execute(
        "SELECT * FROM sales ORDER BY date DESC, id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    return [dict(row) for row in rows]


def create_sale(conn: sqlite3.Connection, dept: str, amount: int, date: str, description: Optional[str]) -> Dict[str, Any]:
    cursor = conn.execute(
        "INSERT INTO sales (dept, amount, date, description) VALUES (?, ?, ?, ?)",
        (dept, amount, date, description),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM sales WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _row_to_dict(row)


def get_sales_period(conn: sqlite3.Connection, start: str, end: str) -> List[Dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT * FROM sales
        WHERE date BETWEEN ? AND ?
        ORDER BY date DESC, id DESC
        """,
        (start, end),
    ).fetchall()
    return [dict(row) for row in rows]


def get_sales_by_dept(conn: sqlite3.Connection, dept_name: str) -> Dict[str, Any]:
    row = conn.execute(
        """
        SELECT dept, SUM(amount) AS total_amount
        FROM sales
        WHERE dept = ?
        GROUP BY dept
        """,
        (dept_name,),
    ).fetchone()
    return _row_to_dict(row) if row else {"dept": dept_name, "total_amount": 0}


def count_employees(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) AS cnt FROM employees").fetchone()
    return int(row["cnt"]) if row else 0


def count_leaves(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) AS cnt FROM leave_balance").fetchone()
    return int(row["cnt"]) if row else 0


def count_sales(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COUNT(*) AS cnt FROM sales").fetchone()
    return int(row["cnt"]) if row else 0


def sum_sales(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM sales").fetchone()
    return int(row["total"]) if row else 0
