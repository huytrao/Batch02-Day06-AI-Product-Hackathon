"""Analytics aggregation for feedback and product-learning metrics."""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from feedback_db import DEFAULT_DB_PATH, connect, init_feedback_db


SUCCESS_OUTCOMES = {"ordered"}
FAILURE_OUTCOMES = {"delayed", "closed", "unavailable"}


def _week_start_iso(days: int = 7) -> str:
    return (datetime.now(timezone.utc) - timedelta(days=days)).replace(microsecond=0).isoformat()


def _rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [dict(row) for row in rows]


def calculate_nps(scores: list[int]) -> float | None:
    if not scores:
        return None
    promoters = sum(1 for score in scores if score >= 9)
    detractors = sum(1 for score in scores if score <= 6)
    return round(((promoters - detractors) / len(scores)) * 100, 1)


def get_feedback_summary(db_path: Path | str = DEFAULT_DB_PATH, days: int = 7) -> dict[str, Any]:
    init_feedback_db(db_path)
    since = _week_start_iso(days)
    with connect(db_path) as conn:
        feedback = _rows_to_dicts(
            conn.execute(
                "SELECT * FROM feedback_submissions WHERE created_at >= ? ORDER BY created_at DESC",
                (since,),
            ).fetchall()
        )
        corrections = _rows_to_dicts(
            conn.execute(
                "SELECT * FROM correction_reports WHERE created_at >= ? ORDER BY created_at DESC",
                (since,),
            ).fetchall()
        )

    total = len(feedback)
    successful = sum(1 for row in feedback if row["outcome"] in SUCCESS_OUTCOMES or row["user_rating"] >= 4)
    failed = sum(1 for row in feedback if row["outcome"] in FAILURE_OUTCOMES or row["user_rating"] <= 2)
    nps_scores = [int(row["nps_score"]) for row in feedback if row["nps_score"] is not None]
    rating_avg = round(sum(row["user_rating"] for row in feedback) / total, 2) if total else None

    queries = Counter(row["query"].strip().lower() for row in feedback if row["query"])
    partners = Counter(row["partner"] or "unknown" for row in feedback)
    confidence = Counter(row["confidence"] or "UNKNOWN" for row in feedback)

    return {
        "period_days": days,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "total_feedback": total,
        "average_rating": rating_avg,
        "accuracy_rate": round(successful / total, 3) if total else None,
        "failure_rate": round(failed / total, 3) if total else None,
        "nps": calculate_nps(nps_scores),
        "top_queries": queries.most_common(10),
        "partner_feedback_count": partners.most_common(),
        "confidence_mix": dict(confidence),
        "pending_corrections": sum(1 for row in corrections if row["review_status"] == "pending"),
        "high_severity_corrections": sum(1 for row in corrections if row["severity"] == "high"),
        "privacy_note": "No names, phone numbers, addresses, emails, or device identifiers are stored.",
    }


def get_partner_performance(partner: str, db_path: Path | str = DEFAULT_DB_PATH, days: int = 7) -> dict[str, Any]:
    init_feedback_db(db_path)
    since = _week_start_iso(days)
    with connect(db_path) as conn:
        feedback = _rows_to_dicts(
            conn.execute(
                """
                SELECT * FROM feedback_submissions
                WHERE created_at >= ? AND lower(partner) = lower(?)
                """,
                (since, partner),
            ).fetchall()
        )
        events = _rows_to_dicts(
            conn.execute(
                """
                SELECT event_type, is_sponsored, COUNT(*) AS count
                FROM partner_events
                WHERE created_at >= ? AND lower(partner) = lower(?)
                GROUP BY event_type, is_sponsored
                """,
                (since, partner),
            ).fetchall()
        )

    total = len(feedback)
    ordered = sum(1 for row in feedback if row["outcome"] == "ordered")
    delayed = sum(1 for row in feedback if row["outcome"] == "delayed")

    return {
        "partner": partner,
        "period_days": days,
        "feedback_count": total,
        "average_rating": round(sum(row["user_rating"] for row in feedback) / total, 2) if total else None,
        "order_success_rate": round(ordered / total, 3) if total else None,
        "delay_report_rate": round(delayed / total, 3) if total else None,
        "event_counts": events,
    }


def write_weekly_report(output_path: Path | str, db_path: Path | str = DEFAULT_DB_PATH, days: int = 7) -> Path:
    report_path = Path(output_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = get_feedback_summary(db_path=db_path, days=days)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report_path


if __name__ == "__main__":
    print(json.dumps(get_feedback_summary(), ensure_ascii=False, indent=2))
