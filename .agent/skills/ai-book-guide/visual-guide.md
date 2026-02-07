# AI 도서 시각 자료 생성 가이드 (Visual System)

본 문서는 도서의 일관된 품질을 위해 이미지 및 도식 생성 시 반드시 준수해야 할 규칙을 정의합니다.

## 1. 마스터 스타일 베이스 (The Master Template v7)

모든 기술 도식은 아래의 프롬프트 베이스를 기반으로 생성합니다.

- **프롬프트**: `A minimalist black and white technical diagram with a strict 16:9 aspect ratio on a solid white background. No shading, no 3D effects, only clean thin line art. The entire assembly of icons, lines, and text is perfectly centered globally within the 16:9 frame, leaving generous and equal white space / margins on all sides (top, bottom, left, right).`

## 2. 핵심 컴포넌트 및 심볼 (Icons & Symbols)

일관성을 위해 다음 키워드를 고정하여 사용합니다.

- **AI 에이전트**: `minimalist line-art brain icon labeled 'AI'`
- **정형 데이터(DB)**: `minimalist line-art cylinder database icon labeled 'MCP (DB)'`
- **비정형 데이터(DOC)**: `minimalist line-art stack of papers icon labeled 'RAG (DOC)'`

## 3. 선과 흐름의 정의 (Line & Arrow)

- **질의 (Query)**: AI에서 대상체로 향하는 얇은 수평 화살표.
- **수집 (Input)**: 여러 소스에서 AI(Brain)로 향하는 얇은 화살표들.
- **결과 (Output)**: AI에서 오른쪽으로 나가는 굵은 수평 화살표.

## 4. 구도 및 여백 (Composition)

- **Safety Margin**: 도식 전체가 화면 캔버스의 60~70% 내외만 차지하도록 설계하여 상하좌우에 충분한 여백을 확보합니다.
- **Global Centering**: 특정 아이콘이 아닌, 전체 조립체의 무게 중심을 16:9 프레임 정중앙에 배치합니다.

---

## 5. 생성 베이스 예시 (V7 Prompts)

1. **하이브리드 처리**: `[Default Style Base] A minimalist line-art brain icon labeled 'AI' is in the exact center. To its left, a minimalist line-art cylinder database icon labeled 'MCP (DB)'. To its right, a minimalist line-art stack of papers icon labeled 'RAG (DOC)'. Connected by thin horizontal lines. The entire three-icon assembly is perfectly centered globally with ample padding.`
2. **요약 및 합성**: `[Default Style Base] In the global center, a minimalist line-art brain icon labeled 'AI'. Multiple thin horizontal arrows labeled 'DATA' point from both sides into it. A single thick horizontal arrow points out from it to the right, labeled 'SYNTHESIS'. Perfect global balance and wide margins.`

---

## 6. 이미지 파일 삽입 및 관리 규칙

도서 원고 내 이미지 삽입 시 플레이스홀더를 사용하지 않고, 실제 파일 경로를 미리 입력합니다. 또한 모든 이미지에는 캡션을 달아야 합니다.

### 6.1 파일 경로 및 관리

- **경로 규칙**: `![이미지 설명](./images/{장번호}_{이미지식별자}.png)`
- **파일명 예시**: `03장_ollama_run.png`, `05장_pdf_parsing_error.png`
- **폴더 관리**: 각 챕터 폴더 내에 `images` 하위 폴더를 생성하여 관리합니다.

### 6.2 캡션 작성 규칙

- **필수 포함**: 이미지 바로 아랫줄에 이탤릭체(`*`)로 캡션을 작성합니다.
- **형식**: `*그림 {장번호}-{순번}: {설명}*`
- **예시**:
  ```markdown
  ![Ollama 실행 화면](./images/03장_ollama_run.png)
  _그림 3-1: Ollama 실행 화면_
  ```
