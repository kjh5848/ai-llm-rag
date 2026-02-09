import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# DB_URL 가져오기 (기본값은 SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./company.db")

# SQLAlchemy Engine 생성
engine = create_engine(DATABASE_URL)

# SessionLocal 클래스 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """FastAPI 종속성 주입을 위한 DB 세션 생성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_connection():
    """기존 raw connection 스타일 코드와의 호환성을 위한 함수"""
    # SQLite인 경우 전용 Row Factory 사용을 위해 직접 연결
    if DATABASE_URL.startswith("sqlite"):
        import sqlite3
        db_path = DATABASE_URL.replace("sqlite:///", "")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        # Postgres 등 다른 DB는 engine.raw_connection() 활용
        return engine.raw_connection()
