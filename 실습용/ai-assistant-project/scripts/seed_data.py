import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import sys

# 프로젝트 루트를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import Base, Employee, LeaveBalance, Sales
from datetime import date

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# SQLite의 경우 check_same_thread 옵션이 필요할 수 있음
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

def init_db():
    print("Creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

def seed_data():
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Seeding data...")
    
    # 1. 직원 정보
    employees = [
        Employee(name="김철수", dept="인사팀", email="chulsoo@company.com", hire_date=date(2022, 1, 1)),
        Employee(name="이영희", dept="영업팀", email="younghee@company.com", hire_date=date(2023, 2, 15)),
        Employee(name="박민수", dept="개발팀", email="minsoo@company.com", hire_date=date(2021, 5, 20)),
        Employee(name="정다은", dept="영업팀", email="daeun@company.com", hire_date=date(2024, 1, 10)),
    ]
    session.add_all(employees)
    session.commit()

    # 2. 휴가 잔여량
    leave_balances = [
        LeaveBalance(employee_id=1, year=2024, total=15, used=5, remaining=10),
        LeaveBalance(employee_id=2, year=2024, total=15, used=2, remaining=13),
        LeaveBalance(employee_id=3, year=2024, total=18, used=10, remaining=8),
        LeaveBalance(employee_id=4, year=2024, total=15, used=0, remaining=15),
    ]
    session.add_all(leave_balances)

    # 3. 매출 데이터
    sales = [
        Sales(dept="영업팀", amount=5000000, date=date(2024, 1, 15), description="A사 계약 체결"),
        Sales(dept="영업팀", amount=3000000, date=date(2024, 1, 20), description="B사 라이선스 갱신"),
        Sales(dept="영업팀", amount=7500000, date=date(2024, 2, 5), description="C사 연간 유지보수"),
        Sales(dept="개발팀", amount=1200000, date=date(2024, 2, 10), description="외부 프로젝트 기술 지원"),
    ]
    session.add_all(sales)
    
    session.commit()
    print("Data seeded successfully.")
    session.close()

if __name__ == "__main__":
    init_db()
    seed_data()
