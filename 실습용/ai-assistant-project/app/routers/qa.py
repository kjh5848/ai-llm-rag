from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.qa_service import qa_service

router = APIRouter(prefix="/admin", tags=["QA"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/qa", response_class=HTMLResponse)
async def qa_page(request: Request):
    return templates.TemplateResponse("qa.html", {
        "request": request,
        "active_page": "qa",
        "results": None
    })

@router.post("/qa/query", response_class=HTMLResponse)
async def qa_query(request: Request, query: str = Form(...)):
    results = qa_service.hybrid_search(query)
    ai_answer = qa_service.get_ai_answer(query, results)
    return templates.TemplateResponse("qa.html", {
        "request": request,
        "active_page": "qa",
        "query": query,
        "results": results,
        "ai_answer": ai_answer
    })
