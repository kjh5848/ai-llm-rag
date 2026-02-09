"""문서별 Q&A 프롬프트(JSONL)를 생성하고 필요 시 LLM 응답까지 만든다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from core.config import PROCESSED_DIR, QA_DIR
from core.llm import LLMError, generate
from core.prompts import render_template


def build_prompts(num_questions: int, output_path: Path, generate_answers: bool) -> int:
    # 문서별로 Q&A 생성 프롬프트를 만들고 파일로 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with output_path.open("w", encoding="utf-8") as out:
        for path in sorted(PROCESSED_DIR.glob("*.md")):
            doc_text = path.read_text(encoding="utf-8")
            doc_id = path.stem
            prompt = render_template(
                "qa_generation_prompt.j2",
                doc_id=doc_id,
                source_path=str(path),
                doc_text=doc_text,
                num_questions=num_questions,
            )
            record = {
                "doc_id": doc_id,
                "prompt": prompt,
            }
            # --generate 옵션이 있으면 즉시 LLM 응답 생성
            if generate_answers:
                try:
                    record["response"] = generate(prompt)
                except LLMError as exc:
                    record["response"] = f"[LLM_ERROR] {exc}"
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
    return count


def main() -> int:
    # CLI 인자 파싱 및 실행
    parser = argparse.ArgumentParser()
    parser.add_argument("--num-questions", type=int, default=5)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--output", type=Path, default=QA_DIR / "qa_tasks.jsonl")
    args = parser.parse_args()

    count = build_prompts(args.num_questions, args.output, args.generate)
    print(f"qa tasks written: {count} docs -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
