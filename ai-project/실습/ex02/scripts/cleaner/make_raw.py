"""processed/*.md를 원본 그대로 복사해 *_raw.md로 저장"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python scripts/make_raw.py <input.md>")
        return 1
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"not found: {src}")
        return 1
    text = src.read_text(encoding="utf-8")
    out = src.with_name(src.stem + "_raw.md")
    out.write_text(text, encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
