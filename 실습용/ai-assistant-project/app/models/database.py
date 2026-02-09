from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dept = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hire_date = Column(Date)

    leave_balances = relationship("LeaveBalance", back_populates="employee")

class LeaveBalance(Base):
    __tablename__ = "leave_balance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    year = Column(Integer, nullable=False)
    total = Column(Float, default=15.0)
    used = Column(Float, default=0.0)
    remaining = Column(Float, default=15.0)

    employee = relationship("Employee", back_populates="leave_balances")

class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    dept = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String)
