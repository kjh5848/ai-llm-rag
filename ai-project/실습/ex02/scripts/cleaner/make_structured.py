"""processed/*.md를 구조화해 *_structured.md로 저장"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def structure_text(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    out_lines = []
    for ln in lines:
        if not ln.strip():
            out_lines.append("")
            continue
        m2 = re.match(r"^(\d+)\.(\d+)\s+(.*)$", ln)
        m = re.match(r"^(\d+)\.\s+(.*)$", ln)
        if m2:
            out_lines.append(f"### {m2.group(1)}.{m2.group(2)} {m2.group(3)}")
            continue
        if m:
            out_lines.append(f"## {m.group(1)}. {m.group(2)}")
            continue
        if ln.startswith("• ") or ln.startswith("•"):
            out_lines.append("- " + ln.lstrip("• ").strip())
            continue
        out_lines.append(ln)
    return "\n".join(out_lines).strip() + "\n"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python scripts/make_structured.py <input.md>")
        return 1
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"not found: {src}")
        return 1
    text = src.read_text(encoding="utf-8")
    out = src.with_name(src.stem + "_structured.md")
    out.write_text(structure_text(text), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
