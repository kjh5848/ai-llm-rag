# PART 1 ~ 3. VectorDB (Chroma) 구축

## 1.3 VectorDB (Chroma) 구축

- 텍스트 추출:
  - `pypdf`
  - `python-docx`
  - `openpyxl`
- Chunking:
  - `RecursiveCharacterTextSplitter`
  - 500~1000자
  - overlap 10~20%
- Embedding:
  - `ko-sroberta-multitask` (한국어 특화 모델)
