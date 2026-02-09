# 05_preprocessing: 지식의 디지털화 실습

본 폴더는 비정형 데이터(PDF, 이미지)를 AI가 읽기 좋은 텍스트 형식으로 변환하는 **전처리(Preprocessing)** 과정을 실습합니다.

## 🛠️ 실습 준비

먼저 필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

## 📝 실습 내용

### 1. PDF 텍스트 추출 (`pdf_parser.py`)

PDF 파일에서 텍스트를 추출하여 `.txt` 파일로 저장합니다.

- **입력**: `data/sample_policy.pdf`
- **출력**: `parsed_data/policy.txt`
- **실행**: `python pdf_parser.py`

### 2. 이미지 캡셔닝 (`image_captioning.py`)

LLaVA 모델을 사용하여 이미지(도표, 차트 등)의 내용을 텍스트로 설명합니다.

- **입력**: `data/chart_sample.png`
- **실행**: `python image_captioning.py`
- **참고**: Ollama가 실행 중이어야 하며, `llava` 모델이 설치되어 있어야 합니다 (`ollama pull llava`).

## 📁 폴더 구조

- `data/`: 실습에 사용되는 원본 데이터 (PDF, PNG)
- `parsed_data/`: 전처리 결과가 저장되는 폴더
- `pdf_parser.py`: PDF 텍스트 추출 스크립트
- `image_captioning.py`: 멀티모달 AI 이미지 분석 스크립트
- `requirements.txt`: 필요한 라이브러리 목록
