"""Request/response evidence logging without personal identifiers.

Use this from a FastAPI app:

    from request_logger import install_request_logger
    install_request_logger(app)

The logger stores compact demo evidence in artifacts/request_response_log.jsonl
and avoids headers, IP addresses, cookies, tokens, phone numbers, and emails.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REQUEST_LOG_PATH = ARTIFACTS_DIR / "request_response_log.jsonl"

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
SECRET_KEYS = {"password", "token", "authorization", "cookie", "phone", "email", "address", "name"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]


def scrub_pii(value: Any) -> Any:
    """Redact obvious PII while preserving fields useful for demo evidence."""
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key).lower()
            if any(secret in key_text for secret in SECRET_KEYS):
                cleaned[key] = "[REDACTED]"
            else:
                cleaned[key] = scrub_pii(item)
        return cleaned
    if isinstance(value, list):
        return [scrub_pii(item) for item in value[:20]]
    if isinstance(value, str):
        text = EMAIL_RE.sub("[EMAIL_REDACTED]", value)
        text = PHONE_RE.sub("[PHONE_REDACTED]", text)
        if len(text) > 500:
            return text[:500] + "...[TRUNCATED]"
        return text
    return value


def append_request_log(entry: dict[str, Any], log_path: Path | str = REQUEST_LOG_PATH) -> Path:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    safe_entry = scrub_pii(entry)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(safe_entry, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def build_log_entry(
    *,
    method: str,
    path: str,
    status_code: int,
    duration_ms: int,
    request_body: Any | None = None,
    response_body: Any | None = None,
) -> dict[str, Any]:
    query_text = ""
    if isinstance(request_body, dict):
        query_text = str(request_body.get("query") or "")
    return {
        "timestamp": utc_now(),
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "query_hash": _hash_text(query_text) if query_text else None,
        "request": scrub_pii(request_body),
        "response": scrub_pii(response_body),
        "privacy_note": "PII redacted; no headers, cookies, IP addresses, or device identifiers stored.",
    }


def install_request_logger(app: Any, log_path: Path | str = REQUEST_LOG_PATH) -> Any:
    """Install FastAPI middleware when FastAPI is available in the project."""
    try:
        from starlette.responses import Response
    except ImportError as exc:  # pragma: no cover - depends on optional FastAPI stack
        raise RuntimeError("FastAPI/Starlette is required to install request logging middleware") from exc

    @app.middleware("http")
    async def request_logging_middleware(request: Any, call_next: Any) -> Any:
        started = time.perf_counter()
        request_body: Any | None = None
        if request.method in {"POST", "PUT", "PATCH"}:
            raw_body = await request.body()
            if raw_body:
                try:
                    request_body = json.loads(raw_body.decode("utf-8"))
                except json.JSONDecodeError:
                    request_body = {"raw_body_hash": _hash_text(raw_body.decode("utf-8", errors="ignore"))}

            async def receive() -> dict[str, Any]:
                return {"type": "http.request", "body": raw_body, "more_body": False}

            request._receive = receive

        response = await call_next(request)
        duration_ms = int((time.perf_counter() - started) * 1000)

        response_body: Any | None = None
        body_chunks = [chunk async for chunk in response.body_iterator]
        body = b"".join(body_chunks)
        if body:
            try:
                response_body = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError:
                response_body = {"body_hash": _hash_text(body.decode("utf-8", errors="ignore"))}

        append_request_log(
            build_log_entry(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                request_body=request_body,
                response_body=response_body,
            ),
            log_path=log_path,
        )

        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    return app
