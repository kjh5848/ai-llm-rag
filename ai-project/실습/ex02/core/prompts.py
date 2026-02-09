"""Jinja2 템플릿 렌더링 유틸."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from core.config import TEMPLATES_DIR

# 템플릿 파일 로더 및 기본 렌더링 옵션
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(name: str, **kwargs: Any) -> str:
    # 템플릿을 렌더링하고 마지막 개행을 보장
    template = _env.get_template(name)
    return template.render(**kwargs).strip() + "\n"


def available_templates() -> list[str]:
    # 현재 템플릿 디렉터리의 .j2 목록 반환
    return [p.name for p in Path(TEMPLATES_DIR).glob("*.j2")]
