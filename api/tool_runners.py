"""Tool runners for the real (LLM) ReAct agent.

These wrap the existing root database layer (``api/db.py`` →
``data/sample_data.sqlite`` with 37 restaurants) and the feedback store so the
LLM agent operates on the same data as the rest of the project.

Tool surface matches ``codebase/artifacts/tools.yaml``:
    query_restaurants, get_eta_estimate, get_evidence, record_feedback, clarify
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from . import db
from . import agent as mock_agent


def query_restaurants(location: str = "Ocean Park 1", max_wait_time: Optional[int] = None) -> List[Dict[str, Any]]:
    """Return restaurant candidates filtered by optional max delivery wait time."""
    rows = db.query_restaurants(location=location, max_wait_time=max_wait_time, limit=5)
    candidates = []
    for r in rows:
        est = mock_agent.tool_get_eta_estimate(r["id"])
        candidates.append(
            {
                "id": r["id"],
                "name": r["name"],
                "location": location,
                "cuisine": r.get("cuisine"),
                "vendor": r.get("vendor"),
                "rating": r.get("rating"),
                "predicted_eta": est["predicted_eta"],
                "confidence": est["confidence"],
            }
        )
    return candidates


def get_eta_estimate(restaurant_id: int) -> Dict[str, Any]:
    """Return predicted delivery ETA and confidence for one restaurant."""
    est = mock_agent.tool_get_eta_estimate(int(restaurant_id))
    return {
        "restaurant_id": int(restaurant_id),
        "predicted_eta": est["predicted_eta"],
        "confidence": est["confidence"],
    }


def get_evidence(restaurant_id: int) -> Dict[str, Any]:
    """Return source links and review evidence for one restaurant."""
    rest = db.get_restaurant_by_id(int(restaurant_id))
    links = db.get_evidence_links(int(restaurant_id))
    if not rest:
        return {"restaurant_id": int(restaurant_id), "source_links": [], "reviews": []}
    return {
        "restaurant_id": int(restaurant_id),
        "source_links": [link["url"] for link in links],
        "reviews": [
            {
                "restaurant": rest["name"],
                "rating": rest.get("rating"),
                "review_count": rest.get("review_count"),
            }
        ],
    }


def record_feedback(query: str, suggestion_id: int, user_rating: int, feedback_text: str = "") -> Dict[str, Any]:
    """Persist user feedback through the feedback store."""
    from .feedback_db import save_feedback

    return save_feedback(
        {
            "query": query,
            "suggestion_id": str(suggestion_id),
            "user_rating": int(user_rating),
            "feedback_text": feedback_text or "",
            "source_context": "react_agent_tool",
        }
    )


def clarify(question: str) -> Dict[str, Any]:
    """Return a clarification request for the next user turn."""
    return {
        "needs_clarification": True,
        "question": question,
        "instruction": "Ask the user this question before calling search tools.",
    }


TOOL_RUNNERS = {
    "query_restaurants": query_restaurants,
    "get_eta_estimate": get_eta_estimate,
    "get_evidence": get_evidence,
    "record_feedback": record_feedback,
    "clarify": clarify,
}


def execute_tool(tool_name: str, params: Dict[str, Any]) -> Any:
    """Dispatch a named tool call with JSON params."""
    if tool_name not in TOOL_RUNNERS:
        raise ValueError(f"Unknown tool: {tool_name}")
    if not isinstance(params, dict):
        raise ValueError("Tool params must be a JSON object")
    return TOOL_RUNNERS[tool_name](**params)
