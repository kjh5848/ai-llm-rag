# PART 1 ~ 3. 기초 인프라 및 데이터 구축

## 1.1 시스템 구성 및 데이터 모델

- Backend: FastAPI + Jinja2 기반의 CRUD 사이트
- DB (PostgreSQL):
  - `employee`: 직원의 기본 정보
  - `leave_balance`: 직원의 연차 잔여 현황
  - `sales`: 부서별 매출 데이터

## 1.2 비정형 문서 수집 및 표준화

- 수집 대상: 사내 규정, 업무 매뉴얼, 기술 문서, FAQ 등 (PDF, Docx, Markdown)
- 표준화:
  - 메타데이터(부서, 버전, 날짜) 부여
  - 섹션 헤더 규칙 통일

## 1.3 CRUD API 구현

### 직원 관리 API
- `POST /employees`: 신규 직원 등록
- `GET /employees/{id}`: 특정 직원 정보 조회
- `PUT /employees/{id}`: 직원 정보 수정
- `DELETE /employees/{id}`: 직원 삭제

### 휴가 관리 API
- `GET /leaves/{emp_id}`: 특정 직원의 잔여 휴가 조회
- `POST /leaves/usage`: 휴가 사용 등록 (잔여량 자동 차감)
- `PUT /leaves/{id}`: 휴가 데이터 강제 수정 (관리자용)

### 매출 관리 API
- `POST /sales`: 매출 데이터 입력
- `GET /sales/period`: 특정 기간별 매출 조회
- `GET /sales/dept/{dept_name}`: 부서별 매출 집계 결과 조회
