"""Ollama 기반 LLM 호출 래퍼."""

from __future__ import annotations

import os
from typing import Any

import requests

from core.config import LLM_MODEL, LLM_TEMPERATURE, OLLAMA_HOST


class LLMError(RuntimeError):
    pass


def generate(prompt: str, model: str | None = None, temperature: float | None = None) -> str:
    # 테스트용으로 MOCK_LLM 환경 변수 지원
    if os.getenv("MOCK_LLM", "false").lower() == "true":
        return "[MOCK_LLM] " + prompt[:800]

    # Ollama /api/generate 요청 포맷
    payload = {
        "model": model or LLM_MODEL,
        "prompt": prompt,
        "temperature": temperature if temperature is not None else LLM_TEMPERATURE,
        "stream": False,
    }
    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=120)
    except requests.RequestException as exc:
        raise LLMError(f"LLM 요청 실패: {exc}") from exc
    if resp.status_code != 200:
        raise LLMError(f"LLM 응답 오류: {resp.status_code} {resp.text}")
    data: dict[str, Any] = resp.json()
    return str(data.get("response", ""))
