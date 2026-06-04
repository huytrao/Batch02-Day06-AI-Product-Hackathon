"""Transparent monetization hooks for partner reporting and sponsored ranking.

Sponsored recommendations are allowed only when they remain explainable and are
clearly labeled in the UI. Sponsorship must not override safety, confidence, or
delivery-speed rules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from analytics import get_partner_performance
from feedback_db import DEFAULT_DB_PATH, record_partner_event


def get_partner_stats(partner: str, db_path: Path | str = DEFAULT_DB_PATH, days: int = 7) -> dict[str, Any]:
    """Return metrics for GET /api/partner-stats?partner=GrabFood."""
    if not partner.strip():
        raise ValueError("partner is required")
    return get_partner_performance(partner=partner.strip(), db_path=db_path, days=days)


def log_partner_impression(
    partner: str,
    suggestion_id: str | None = None,
    *,
    is_sponsored: bool = False,
    db_path: Path | str = DEFAULT_DB_PATH,
) -> dict[str, str]:
    return record_partner_event(
        {
            "partner": partner,
            "suggestion_id": suggestion_id,
            "event_type": "sponsored_impression" if is_sponsored else "impression",
            "is_sponsored": is_sponsored,
        },
        db_path=db_path,
    )


def apply_sponsorship_label(suggestion: dict[str, Any], sponsored_partners: set[str]) -> dict[str, Any]:
    """Decorate, never secretly boost, a suggestion from a sponsored partner."""
    partner = suggestion.get("partner") or suggestion.get("vendor")
    is_sponsored = bool(partner and partner in sponsored_partners)
    decorated = dict(suggestion)
    decorated["is_sponsored"] = is_sponsored
    decorated["sponsorship_disclosure"] = "Sponsored partner" if is_sponsored else None
    return decorated


def eligible_for_sponsored_slot(suggestion: dict[str, Any]) -> bool:
    """Guardrail for monetization: LOW confidence cannot be promoted."""
    return str(suggestion.get("confidence", "")).upper() in {"HIGH", "MEDIUM"}
