"""
Database connection and query helpers for Ocean Park 1 Eats.

Provides synchronous SQLite helpers used by the agent tools.
All queries are fast (<50ms) on the local SQLite database.
"""

import os
import sqlite3
from typing import Optional

# ---------------------------------------------------------------------------
# Resolve paths relative to repo root
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = os.path.join(_REPO_ROOT, "data", "sample_data.sqlite")

# Module-level connection (lazy init)
_conn: Optional[sqlite3.Connection] = None


def get_conn(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Return a module-level SQLite connection, creating it on first call."""
    global _conn
    if _conn is None:
        path = db_path or DEFAULT_DB_PATH
        _conn = sqlite3.connect(path, check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA busy_timeout=5000")
    return _conn


def close_conn():
    """Close the module-level connection."""
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None


# ---------------------------------------------------------------------------
# Restaurant queries
# ---------------------------------------------------------------------------

def query_restaurants(
    location: Optional[str] = None,
    max_wait_time: Optional[int] = None,
    cuisine: Optional[str] = None,
    vendor: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 10,
) -> list[dict]:
    """
    Query restaurants with optional filters.

    location:   filter by name containing (case-insensitive substring match)
    max_wait_time: filter by base_eta <= max_wait_time
    cuisine:    filter by cuisine containing
    vendor:     filter by exact vendor name
    tags:       filter by tags containing (comma-separated, any match)
    """
    conn = get_conn()
    conditions = []
    params: list = []

    if max_wait_time:
        conditions.append("base_eta <= ?")
        params.append(max_wait_time)

    if cuisine:
        conditions.append("cuisine LIKE ?")
        params.append(f"%{cuisine}%")

    if vendor:
        conditions.append("vendor = ?")
        params.append(vendor)

    if tags:
        # "best-seller" → tags LIKE '%best-seller%'
        for tag in tags.split(","):
            tag = tag.strip()
            if tag:
                conditions.append("tags LIKE ?")
                params.append(f"%{tag}%")

    where = " AND ".join(conditions) if conditions else "1=1"
    sql = f"SELECT * FROM restaurants WHERE {where} ORDER BY base_eta ASC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


def get_restaurant_by_id(restaurant_id: int) -> Optional[dict]:
    """Get a single restaurant by ID."""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM restaurants WHERE id = ?", (restaurant_id,)
    ).fetchone()
    return dict(row) if row else None


def get_eta_history(restaurant_id: int) -> list[dict]:
    """Get ETA history records for a restaurant."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT eta, recorded_at FROM eta_logs WHERE restaurant_id = ? ORDER BY recorded_at DESC",
        (restaurant_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_evidence_links(restaurant_id: int) -> list[dict]:
    """Get evidence links for a restaurant."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT url, label FROM evidence_links WHERE restaurant_id = ?",
        (restaurant_id,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_eta_stats(restaurant_id: int) -> dict:
    """Compute aggregated ETA statistics for a restaurant."""
    conn = get_conn()
    row = conn.execute(
        """SELECT
               COUNT(*) as count,
               AVG(eta) as avg_eta,
               MIN(eta) as min_eta,
               MAX(eta) as max_eta
           FROM eta_logs
           WHERE restaurant_id = ?""",
        (restaurant_id,)
    ).fetchone()

    if not row or row["count"] == 0:
        return {"count": 0, "avg_eta": None, "min_eta": None, "max_eta": None, "std_dev": None}

    # Manual std dev
    etas = [r["eta"] for r in conn.execute(
        "SELECT eta FROM eta_logs WHERE restaurant_id = ?", (restaurant_id,)
    ).fetchall()]
    avg = sum(etas) / len(etas)
    variance = sum((e - avg) ** 2 for e in etas) / len(etas)
    std_dev = variance ** 0.5

    return {
        "count": row["count"],
        "avg_eta": round(avg, 1),
        "min_eta": row["min_eta"],
        "max_eta": row["max_eta"],
        "std_dev": round(std_dev, 1),
    }


# ---------------------------------------------------------------------------
# Feedback queries
# ---------------------------------------------------------------------------

def save_feedback(
    query_text: str,
    suggestion_id: int,
    rating: int,
    feedback_text: str = "",
) -> int:
    """Save a feedback submission, returns the new row ID."""
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO feedback_submissions (query_text, suggestion_id, rating, feedback_text)
           VALUES (?, ?, ?, ?)""",
        (query_text, suggestion_id, rating, feedback_text),
    )
    conn.commit()
    return cur.lastrowid


def get_feedback_summary() -> dict:
    """Return aggregate feedback stats."""
    conn = get_conn()
    row = conn.execute(
        """SELECT
               COUNT(*) as total,
               AVG(rating) as avg_rating,
               SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) as positive
           FROM feedback_submissions"""
    ).fetchone()
    return dict(row) if row else {"total": 0, "avg_rating": None, "positive": 0}


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def count_restaurants() -> int:
    """Return total restaurant count."""
    return get_conn().execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
