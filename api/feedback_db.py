"""Feedback persistence for Ocean Park 1 Eats.

This module owns the feedback database used by Member E. It deliberately stores
only product-learning signals and avoids personal identifiers.
"""

from __future__ import annotations

import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "feedback.sqlite"


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS feedback_submissions (
    feedback_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    query TEXT NOT NULL,
    location TEXT,
    suggestion_id TEXT NOT NULL,
    suggestion_name TEXT,
    partner TEXT,
    predicted_eta_min INTEGER,
    confidence TEXT CHECK (confidence IN ('HIGH', 'MEDIUM', 'LOW') OR confidence IS NULL),
    user_rating INTEGER NOT NULL CHECK (user_rating BETWEEN 1 AND 5),
    nps_score INTEGER CHECK (nps_score BETWEEN 0 AND 10 OR nps_score IS NULL),
    outcome TEXT NOT NULL DEFAULT 'unknown'
        CHECK (outcome IN ('ordered', 'skipped', 'delayed', 'closed', 'unavailable', 'unknown')),
    feedback_text TEXT,
    source_context TEXT,
    metadata_json TEXT
);

CREATE TABLE IF NOT EXISTS correction_reports (
    report_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    suggestion_id TEXT NOT NULL,
    report_type TEXT NOT NULL,
    user_note TEXT,
    evidence_link TEXT,
    review_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (review_status IN ('pending', 'accepted', 'rejected')),
    severity TEXT NOT NULL DEFAULT 'medium'
        CHECK (severity IN ('low', 'medium', 'high'))
);

CREATE TABLE IF NOT EXISTS partner_events (
    event_id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    partner TEXT NOT NULL,
    suggestion_id TEXT,
    event_type TEXT NOT NULL
        CHECK (event_type IN ('impression', 'open_app', 'call_vendor', 'sponsored_impression', 'conversion')),
    is_sponsored INTEGER NOT NULL DEFAULT 0 CHECK (is_sponsored IN (0, 1)),
    metadata_json TEXT
);

CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback_submissions(created_at);
CREATE INDEX IF NOT EXISTS idx_feedback_partner ON feedback_submissions(partner);
CREATE INDEX IF NOT EXISTS idx_feedback_query ON feedback_submissions(query);
CREATE INDEX IF NOT EXISTS idx_partner_events_partner ON partner_events(partner);
"""


@dataclass(frozen=True)
class FeedbackSubmission:
    query: str
    suggestion_id: str
    user_rating: int
    location: str | None = None
    suggestion_name: str | None = None
    partner: str | None = None
    predicted_eta_min: int | None = None
    confidence: str | None = None
    nps_score: int | None = None
    outcome: str = "unknown"
    feedback_text: str | None = None
    source_context: str | None = None
    metadata_json: str | None = None


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def connect(db_path: Path | str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_feedback_db(db_path: Path | str = DEFAULT_DB_PATH) -> Path:
    path = Path(db_path)
    with connect(path) as conn:
        conn.executescript(SCHEMA_SQL)
    return path


def save_feedback(payload: FeedbackSubmission | dict[str, Any], db_path: Path | str = DEFAULT_DB_PATH) -> dict[str, str]:
    init_feedback_db(db_path)
    data = payload.__dict__ if isinstance(payload, FeedbackSubmission) else dict(payload)
    rating = int(data["user_rating"])
    if rating < 1 or rating > 5:
        raise ValueError("user_rating must be between 1 and 5")

    confidence = data.get("confidence")
    if confidence:
        confidence = str(confidence).upper()

    feedback_id = data.get("feedback_id") or f"fb_{uuid.uuid4().hex[:12]}"
    row = {
        "feedback_id": feedback_id,
        "created_at": data.get("created_at") or utc_now(),
        "query": data["query"],
        "location": data.get("location"),
        "suggestion_id": str(data["suggestion_id"]),
        "suggestion_name": data.get("suggestion_name"),
        "partner": data.get("partner"),
        "predicted_eta_min": data.get("predicted_eta_min"),
        "confidence": confidence,
        "user_rating": rating,
        "nps_score": data.get("nps_score"),
        "outcome": data.get("outcome") or "unknown",
        "feedback_text": data.get("feedback_text"),
        "source_context": data.get("source_context"),
        "metadata_json": data.get("metadata_json"),
    }

    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO feedback_submissions (
                feedback_id, created_at, query, location, suggestion_id, suggestion_name,
                partner, predicted_eta_min, confidence, user_rating, nps_score,
                outcome, feedback_text, source_context, metadata_json
            ) VALUES (
                :feedback_id, :created_at, :query, :location, :suggestion_id, :suggestion_name,
                :partner, :predicted_eta_min, :confidence, :user_rating, :nps_score,
                :outcome, :feedback_text, :source_context, :metadata_json
            )
            """,
            row,
        )
    return {"status": "saved", "feedback_id": feedback_id}


def save_correction(payload: dict[str, Any], db_path: Path | str = DEFAULT_DB_PATH) -> dict[str, str]:
    init_feedback_db(db_path)
    report_id = payload.get("report_id") or f"cr_{uuid.uuid4().hex[:12]}"
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO correction_reports (
                report_id, created_at, suggestion_id, report_type, user_note,
                evidence_link, review_status, severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                report_id,
                payload.get("created_at") or utc_now(),
                str(payload["suggestion_id"]),
                payload["report_type"],
                payload.get("user_note"),
                payload.get("evidence_link"),
                payload.get("review_status", "pending"),
                payload.get("severity", "medium"),
            ),
        )
    return {"status": "saved", "report_id": report_id}


def record_partner_event(payload: dict[str, Any], db_path: Path | str = DEFAULT_DB_PATH) -> dict[str, str]:
    init_feedback_db(db_path)
    event_id = payload.get("event_id") or f"pe_{uuid.uuid4().hex[:12]}"
    with connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO partner_events (
                event_id, created_at, partner, suggestion_id, event_type, is_sponsored, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                payload.get("created_at") or utc_now(),
                payload["partner"],
                payload.get("suggestion_id"),
                payload["event_type"],
                1 if payload.get("is_sponsored") else 0,
                payload.get("metadata_json"),
            ),
        )
    return {"status": "saved", "event_id": event_id}


if __name__ == "__main__":
    print(f"Initialized feedback database: {init_feedback_db()}")
