# Cleaner Scripts

정제/구조화 스크립트 모음입니다.

## 파일
- `make_raw.py`: 원본 그대로 복사해서 `_raw.md` 생성
- `make_clean.py`: 헤더/페이지 번호 제거 + 줄바꿈/공백 정리
- `make_structured.py`: 제목/소제목 구조화 + bullet 정리

## 사용 예시
```bash
PYTHONPATH=. python scripts/cleaner/make_raw.py data/processed/HR_사내규정_v1.0_b24e9179.md
PYTHONPATH=. python scripts/cleaner/make_clean.py data/processed/HR_사내규정_v1.0_b24e9179.md
PYTHONPATH=. python scripts/cleaner/make_structured.py data/processed/HR_사내규정_v1.0_b24e9179.md
```
