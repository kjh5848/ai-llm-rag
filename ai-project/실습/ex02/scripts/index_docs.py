from __future__ import annotations

import sys

from scripts.vectorizer.chroma_indexer import index_processed


def main() -> int:
    total = index_processed()
    if total == 0:
        print("no processed documents found. run scripts/ingest.py first")
        return 1
    print(f"indexed chunks: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
