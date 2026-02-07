from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 목데이터 (Sample Data)
mock_chat_history = [
    {"role": "ai", "content": "안녕하세요! <b>Metacoding AI</b> 업무 비서입니다. 사내 인사 정보와 매출 데이터를 통합하여 답변해 드립니다."},
    {"role": "user", "content": "올해 내 남은 연차 일수와 우리 팀 평균 연차 사용률을 비교해줘."},
    {"role": "ai", "content": "kjh님의 잔여 연차는 **12일**입니다. 팀 평균 연차 사용률은 65%이며, kjh님은 현재 40%로 팀 평균보다 조금 낮게 사용 중이시네요.", "source": "직원 DB & 휴가 관리 시스템"}
]

mock_thought_process = [
    {"time": "11:52:01", "action": "사용자 매핑: admin_kjh 확인"},
    {"time": "11:52:03", "action": "MCP 도구 호출: get_remaining_leave(user_id='kjh')"},
    {"time": "11:52:05", "action": "SQL 쿼리 실행: SELECT AVG(usage) FROM leave_table..."},
    {"time": "11:52:06", "action": "데이터 병합 및 DeepSeek R1 답변 생성"}
]

@app.get("/")
@app.get("/phase2")
async def phase2(request: Request):
    return templates.TemplateResponse("phase2_dashboard.html", {
        "request": request,
        "active_page": "phase2",
        "doc_count": "5,620"
    })

@app.get("/phase3")
async def phase3(request: Request):
    return templates.TemplateResponse("phase3_chat.html", {
        "request": request,
        "active_page": "phase3",
        "chat_history": mock_chat_history,
        "thought_process": mock_thought_process
    })

if __name__ == "__main__":
    print("FastAPI 서버 시작: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
