"""FastAPI routes for Member E feedback, analytics, and monetization outputs."""

from __future__ import annotations

from typing import Any

from analytics import get_feedback_summary
from feedback_db import save_feedback
from monetization import get_partner_stats


def create_feedback_router() -> Any:
    """Return an APIRouter if FastAPI is installed.

    Member C can add this to the main app:

        from feedback_routes import create_feedback_router
        app.include_router(create_feedback_router(), prefix="/api")
    """
    try:
        from fastapi import APIRouter, HTTPException, Query
        from pydantic import BaseModel, Field
    except ImportError as exc:  # pragma: no cover - optional API dependency
        raise RuntimeError("FastAPI and Pydantic are required for feedback routes") from exc

    class FeedbackPayload(BaseModel):
        query: str = Field(min_length=1)
        suggestion_id: str = Field(min_length=1)
        user_rating: int = Field(ge=1, le=5)
        location: str | None = None
        suggestion_name: str | None = None
        partner: str | None = None
        predicted_eta_min: int | None = None
        confidence: str | None = None
        nps_score: int | None = Field(default=None, ge=0, le=10)
        outcome: str = "unknown"
        feedback_text: str | None = None
        source_context: str | None = None
        metadata_json: str | None = None

    router = APIRouter()

    @router.post("/feedback")
    def post_feedback(payload: FeedbackPayload) -> dict[str, str]:
        try:
            data = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
            return save_feedback(data)
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @router.get("/analytics")
    def get_analytics(days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
        return get_feedback_summary(days=days)

    @router.get("/partner-stats")
    def partner_stats(partner: str, days: int = Query(default=7, ge=1, le=90)) -> dict[str, Any]:
        try:
            return get_partner_stats(partner=partner, days=days)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return router
