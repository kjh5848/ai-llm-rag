from pydantic import BaseModel
from typing import Optional


class EmployeeCreate(BaseModel):
    name: str
    dept: str
    email: str
    hire_date: str


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    dept: Optional[str] = None
    email: Optional[str] = None
    hire_date: Optional[str] = None


class LeaveUsage(BaseModel):
    employee_id: int
    days: float


class LeaveUpdate(BaseModel):
    employee_id: Optional[int] = None
    year: Optional[int] = None
    total: Optional[float] = None
    used: Optional[float] = None
    remaining: Optional[float] = None


class SalesCreate(BaseModel):
    dept: str
    amount: int
    date: str
    description: Optional[str] = None
