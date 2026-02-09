import os
import sqlite3
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv()

DEFAULT_DB_URL = "sqlite:///./company.db"
DB_URL = os.getenv("DB_URL", DEFAULT_DB_URL)


def _db_path_from_url(url: str) -> str:
    if url.startswith("sqlite:///"):
        raw_path = url.replace("sqlite:///", "", 1)
        if raw_path.startswith("./"):
            return os.path.join(BASE_DIR, raw_path[2:])
        if raw_path.startswith("/"):
            return raw_path
        return os.path.join(BASE_DIR, raw_path)
    # Fallback: treat as relative path
    return os.path.join(BASE_DIR, "company.db")


DB_PATH = _db_path_from_url(DB_URL)


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
