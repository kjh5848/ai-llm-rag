"""정형 데이터용 PostgreSQL 스키마/시드 래퍼."""

from __future__ import annotations

from core.db import init_db, seed_db


__all__ = ["init_db", "seed_db"]
