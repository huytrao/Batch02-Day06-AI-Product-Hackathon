"""FastAPI routes for Member E feedback, analytics, and monetization outputs.

These routes are mounted by ``api/app.py`` and own the persistent feedback
store (``data/feedback.sqlite``), weekly analytics, and partner reporting.

The feedback endpoint accepts both the rich schema used by
``web/feedback-widget.js`` (``user_rating``/``feedback_text``) and the compact
payload sent by ``web/app.js`` (``rating``/``text``) so the whole frontend can
submit feedback without changes.
"""

from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field, model_validator

from .analytics import get_feedback_summary
from .feedback_db import save_feedback
from .monetization import get_partner_stats


class FeedbackPayload(BaseModel):
    """Flexible feedback payload.

    Accepts ``user_rating`` (canonical) or ``rating`` (compact frontend),
    and ``feedback_text`` (canonical) or ``text`` (compact frontend).
    """

    query: str = Field(min_length=1)
    suggestion_id: str = Field(min_length=1)
    user_rating: Optional[int] = Field(default=None, ge=1, le=5)
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    location: Optional[str] = None
    suggestion_name: Optional[str] = None
    partner: Optional[str] = None
    predicted_eta_min: Optional[int] = None
    confidence: Optional[str] = None
    nps_score: Optional[int] = Field(default=None, ge=0, le=10)
    outcome: str = "unknown"
    feedback_text: Optional[str] = None
    text: Optional[str] = None
    source_context: Optional[str] = None
    metadata_json: Optional[str] = None

    @model_validator(mode="after")
    def _coalesce_aliases(self) -> "FeedbackPayload":
        if self.user_rating is None:
            self.user_rating = self.rating
        if self.user_rating is None:
            raise ValueError("rating (1-5) is required")
        if self.feedback_text is None:
            self.feedback_text = self.text
        # suggestion_id is stored as text in the feedback DB
        self.suggestion_id = str(self.suggestion_id)
        return self


def create_feedback_router() -> APIRouter:
    """Return the APIRouter for feedback, analytics, and partner stats."""
    router = APIRouter()

    @router.post("/feedback")
    def post_feedback(payload: FeedbackPayload) -> dict[str, str]:
        try:
            data = payload.model_dump()
            # Drop compact aliases so they don't leak into the DB layer
            data.pop("rating", None)
            data.pop("text", None)
            return save_feedback(data)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # pragma: no cover - defensive
            raise HTTPException(status_code=500, detail=str(exc)) from exc

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
