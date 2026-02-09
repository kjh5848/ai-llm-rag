"""processed/*.md를 정제해 *_clean.md로 저장"""

from __future__ import annotations

import re
import sys
from pathlib import Path


HEADER_RE = re.compile(r"^Metacoding Inc\. - Future Operations Policy\s*$")
PAGE_NUM_RE = re.compile(r"^\d+\s*$")


def clean_text(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines()]
    filtered = []
    for ln in lines:
        if HEADER_RE.match(ln):
            continue
        if PAGE_NUM_RE.match(ln):
            continue
        filtered.append(ln)

    joined = []
    i = 0
    while i < len(filtered):
        line = filtered[i].strip()
        if not line:
            joined.append("")
            i += 1
            continue
        if i + 1 < len(filtered):
            nxt = filtered[i + 1].strip()
            nxt_is_bullet = nxt.startswith("•") or nxt.startswith("-")
            nxt_is_heading = bool(re.match(r"^\d+(\.\d+)*\s+", nxt))
            if (not re.search(r"[\.!\?\:]$", line)) and nxt and not nxt_is_bullet and not nxt_is_heading:
                line = line + " " + nxt
                i += 2
                while i < len(filtered):
                    nxt2 = filtered[i].strip()
                    if not nxt2:
                        break
                    nxt2_is_bullet = nxt2.startswith("•") or nxt2.startswith("-")
                    nxt2_is_heading = bool(re.match(r"^\d+(\.\d+)*\s+", nxt2))
                    if (not re.search(r"[\.!\?\:]$", line)) and not nxt2_is_bullet and not nxt2_is_heading:
                        line = line + " " + nxt2
                        i += 1
                    else:
                        break
                joined.append(line)
                continue
        joined.append(line)
        i += 1

    cleaned_lines = [re.sub(r"\s+", " ", ln).strip() if ln.strip() else "" for ln in joined]
    cleaned = []
    prev_blank = False
    for ln in cleaned_lines:
        if not ln:
            if not prev_blank:
                cleaned.append("")
            prev_blank = True
        else:
            cleaned.append(ln)
            prev_blank = False

    return "\n".join(cleaned).strip() + "\n"


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python scripts/make_clean.py <input.md>")
        return 1
    src = Path(sys.argv[1])
    if not src.exists():
        print(f"not found: {src}")
        return 1
    text = src.read_text(encoding="utf-8")
    out = src.with_name(src.stem + "_clean.md")
    out.write_text(clean_text(text), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
