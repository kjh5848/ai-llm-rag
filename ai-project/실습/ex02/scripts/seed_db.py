"""정형 DB에 샘플 데이터를 적재하는 스크립트."""

from __future__ import annotations

import sys

from mcp.db import seed_db


def main() -> int:
    # 스키마 생성 + 샘플 데이터 삽입
    seed_db()
    print("seeded structured.db")
    return 0


if __name__ == "__main__":
    sys.exit(main())
