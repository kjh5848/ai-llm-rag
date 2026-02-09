"""Jinja2 템플릿 설정 (FastAPI UI용)."""

from __future__ import annotations

from fastapi.templating import Jinja2Templates

from core.config import TEMPLATES_DIR


templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
