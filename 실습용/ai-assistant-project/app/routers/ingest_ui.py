from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.ingest_service import ingest_service

router = APIRouter(prefix="/admin", tags=["Ingest UI"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/ingest", response_class=HTMLResponse)
async def ingest_page(request: Request):
    """인제스트 관리 페이지"""
    files = ingest_service.get_file_status()
    return templates.TemplateResponse("ingest.html", {
        "request": request, 
        "files": files,
        "active_page": "ingest"
    })

@router.post("/ingest/convert")
async def ingest_convert(file_path: str = Form(...)):
    """파일을 마크다운으로 변환합니다 (IngestService 이용)"""
    file_name = os.path.basename(file_path)
    ingest_service.run_convert(file_name)
    return RedirectResponse(url="/admin/ingest", status_code=303)

@router.post("/ingest/embed")
async def ingest_embed(md_path: str = Form(...)):
    """마크다운 파일을 벡터 DB에 임베딩합니다 (IngestService 이용)"""
    ingest_service.run_embed()
    return RedirectResponse(url="/admin/ingest", status_code=303)

import os # os name for basename inside function helper if needed, but better placed at top
