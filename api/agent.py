"""
ReAct Agent for Ocean Park 1 Eats prototype.

Implements a simple Reasoning-Action loop that uses database tools to answer
user queries about fast food delivery options.

The agent follows the ReAct pattern:
- Think: reason about what to do next
- Act: select and execute a tool
- Observe: incorporate tool results
- Repeat until a final answer can be synthesized.

Tools available:
- query_restaurants: filter restaurants by location, max_wait_time, etc.
- get_eta_estimate: get predicted ETA and confidence for a restaurant
- get_evidence: get source links/evidence for a restaurant
- record_feedback: log user feedback (not used in query flow)
- clarify: ask clarifying question (not implemented in this mock)

The agent returns a structured response with:
- suggestions: list of ranked restaurant suggestions
- action_trace: step-by-step reasoning and actions taken
- execution_time_ms: total time taken
"""

import time
import json
from typing import List, Dict, Any, Optional
from . import db

# ---------------------------------------------------------------------------
# Tool implementations (thin wrappers around db.py)
# ---------------------------------------------------------------------------

def tool_query_restaurants(
    location: Optional[str] = None,
    max_wait_time: Optional[int] = None,
    cuisine: Optional[str] = None,
    vendor: Optional[str] = None,
    tags: Optional[str] = None,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """Tool: query restaurants with optional filters."""
    return db.query_restaurants(
        location=location,
        max_wait_time=max_wait_time,
        cuisine=cuisine,
        vendor=vendor,
        tags=tags,
        limit=limit,
    )


def tool_get_eta_estimate(restaurant_id: int) -> Dict[str, Any]:
    """
    Tool: get ETA estimate and confidence for a restaurant.
    Uses historical ETA data to compute prediction and confidence.
    """
    stats = db.get_eta_stats(restaurant_id)
    if stats["count"] == 0:
        # No history: fallback to base_eta from restaurant record
        rest = db.get_restaurant_by_id(restaurant_id)
        if not rest:
            return {"predicted_eta": 30, "confidence": 0.1, "eta_history_count": 0}
        base = rest["base_eta"]
        return {
            "predicted_eta": base,
            "confidence": 0.3,  # low confidence because no history
            "eta_history_count": 0,
            "base_eta": base,
        }

    # Use historical average as prediction
    predicted_eta = stats["avg_eta"]
    # Confidence: inverse of normalized std dev (lower std dev -> higher confidence)
    # clamp confidence between 0.5 and 0.95
    if stats["std_dev"] is None or stats["std_dev"] == 0:
        confidence = 0.95
    else:
        # Normalize std dev by mean to get coefficient of variation
        cv = stats["std_dev"] / stats["avg_eta"] if stats["avg_eta"] > 0 else 1
        # Map cv [0, 1+] to confidence [0.95, 0.5]
        confidence = max(0.5, 0.95 - (cv * 0.45))
        confidence = min(0.95, confidence)

    return {
        "predicted_eta": round(predicted_eta),
        "confidence": round(confidence, 2),
        "eta_history_count": stats["count"],
        "min_eta": stats["min_eta"],
        "max_eta": stats["max_eta"],
        "std_dev": stats["std_dev"],
    }


def tool_get_evidence(restaurant_id: int) -> List[Dict[str, Any]]:
    """Tool: get evidence links for a restaurant."""
    return db.get_evidence_links(restaurant_id)


def tool_record_feedback(
    query_text: str,
    suggestion_id: int,
    rating: int,
    feedback_text: str = "",
) -> int:
    """Tool: record user feedback."""
    return db.save_feedback(query_text, suggestion_id, rating, feedback_text)


def tool_clarify(question: str) -> Dict[str, Any]:
    """
    Tool: ask a clarifying question.
    In this mock implementation, we simply return the question.
    In a real system, this would pause the agent and wait for user input.
    """
    return {"question": question, "status": "awaiting_clarification"}


# ---------------------------------------------------------------------------
# Agent state and reasoning
# ---------------------------------------------------------------------------

class ReActAgent:
    def __init__(self):
        self.action_trace: List[Dict[str, Any]] = []
        self.step_counter = 0

    def _think(self, thought: str) -> None:
        """Record a thinking step."""
        self.step_counter += 1
        self.action_trace.append({
            "step": self.step_counter,
            "type": "think",
            "thought": thought,
        })

    def _act(self, tool_name: str, params: Dict[str, Any], result: Any) -> None:
        """Record an action step."""
        self.step_counter += 1
        self.action_trace.append({
            "step": self.step_counter,
            "type": "action",
            "tool": tool_name,
            "params": params,
            "result": result,
        })

    def run(self, query: str, location: str = "Ocean Park 1") -> Dict[str, Any]:
        """
        Execute the ReAct loop for a user query.
        Returns a dictionary with suggestions, action_trace, and execution_time_ms.
        """
        start_time = time.time()
        self.action_trace = []
        self.step_counter = 0

        # Initial thought
        self._think(
            f"User wants: '{query}' near {location}. "
            f"I need to find restaurants that match the query and estimate delivery time."
        )

        # Step 1: Query restaurants based on query keywords
        # Simple keyword matching: we'll treat the query as a cuisine or tag hint
        query_lower = query.lower()
        # Heuristic: if query contains speed-related words, prioritize low eta
        speed_keywords = ["nhanh", "fast", "quick", "giao nhanh", "express", "gấp"]
        max_wait_time = 45 if any(k in query_lower for k in speed_keywords) else 60

        # Try to infer cuisine from query
        cuisine_map = {
            "phở": "Phở - Món Việt",
            "bún": "Bún - Món Việt",
            "cơm": "Cơm - Món Việt",
            "pizza": "Pizza - Ý",
            "sushi": "Sushi - Nhật",
            "mì": "Mì - Hàn Quốc",
            "gà": "Gà - Món Việt",
            "bò": "Bò - Món Việt",
            "cháo": "Cháo - Món Việt",
            "lẩu": "Lẩu - Món Việt",
            "xôi": "Xôi - Món Việt",
            "bánh mì": "Bánh mì - Đồ ăn nhanh",
            "bánh cuốn": "Bánh - Món Việt",
            "bánh xèo": "Bánh - Món Nam",
            "bánh giò": "Bánh - Món Việt",
            "chả cá": "Cá - Món Việt",
            "hủ tiếu": "Hủ tiếu - Món Nam",
            "mỳ quảng": "Mỳ - Món Trung Bộ",
            "cáy": "Cáy - Món Việt",  # not used but placeholder
        }
        inferred_cuisine = None
        for keyword, cuisine_name in cuisine_map.items():
            if keyword in query_lower:
                inferred_cuisine = cuisine_name
                break

        # If no cuisine inferred, maybe it's a general snack/drink
        if not inferred_cuisine:
            snack_keywords = ["trà", "nước", "đồ uống", "snack", "vặt"]
            if any(k in query_lower for k in snack_keywords):
                inferred_cuisine = "Đồ uống"  # we have Trà Chanh 1989

        restaurants = tool_query_restaurants(
            location=location,
            max_wait_time=max_wait_time,
            cuisine=inferred_cuisine,
            limit=20,  # get a good pool to rank
        )

        self._act(
            "query_restaurants",
            {
                "location": location,
                "max_wait_time": max_wait_time,
                "cuisine": inferred_cuisine,
                "limit": 20,
            },
            {
                "count": len(restaurants),
                "sample_ids": [r["id"] for r in restaurants[:5]],
            },
        )

        if not restaurants:
            self._think(
                "No restaurants found matching the criteria. "
                "I will broaden the search by removing cuisine filter and increasing max wait time."
            )
            restaurants = tool_query_restaurants(
                location=location,
                max_wait_time=90,  # broaden
                limit=20,
            )
            self._act(
                "query_restaurants",
                {"location": location, "max_wait_time": 90, "limit": 20},
                {"count": len(restaurants)},
            )

        # Step 2: For each restaurant, get ETA estimate and evidence
        # We'll score each restaurant by: (confidence * inverse_eta) to prefer fast & confident
        scored = []
        for rest in restaurants:
            eta_est = tool_get_eta_estimate(rest["id"])
            evidence = tool_get_evidence(rest["id"])
            # Compute a simple score: higher confidence and lower eta -> higher score
            # normalize eta: assume 0-120 min range, score = confidence * (1 - eta/120)
            eta_norm = min(eta_est["predicted_eta"] / 120.0, 1.0)
            score = eta_est["confidence"] * (1 - eta_norm)  # higher is better
            scored.append(
                {
                    "restaurant": rest,
                    "eta_estimate": eta_est,
                    "evidence": evidence,
                    "score": score,
                }
            )

        self._act(
            "get_eta_estimate_and_evidence",
            {"restaurant_count": len(restaurants)},
            {
                "scored_count": len(scored),
                "top_score": round(scored[0]["score"], 3) if scored else 0,
            },
        )

        # Step 3: Sort by score and pick top 2
        scored.sort(key=lambda x: x["score"], reverse=True)
        top_n = min(2, len(scored))
        top_picks = scored[:top_n]

        self._think(
            f"Scored {len(scored)} candidates. Selected top {top_n} for final suggestions."
        )

        # Build final suggestions
        suggestions = []
        for pick in top_picks:
            rest = pick["restaurant"]
            eta_est = pick["eta_estimate"]
            evidence = pick["evidence"]
            suggestions.append(
                {
                    "id": rest["id"],
                    "name": rest["name"],
                    "vendor": rest["vendor"],
                    "predicted_eta": eta_est["predicted_eta"],
                    "confidence": eta_est["confidence"],
                    "evidence_links": [e["url"] for e in evidence],
                    "cuisine": rest["cuisine"],
                    "tags": rest["tags"].split(",") if rest["tags"] else [],
                }
            )

        self._act(
            "finalize_suggestions",
            {"suggestion_count": len(suggestions)},
            {
                "suggestions": [
                    {"id": s["id"], "name": s["name"], "eta": s["predicted_eta"]}
                    for s in suggestions
                ]
            },
        )

        # Final thought
        self._think(
            f"Generated {len(suggestions)} suggestions. "
            f"Each includes predicted ETA, confidence score, and evidence links."
        )

        execution_time_ms = int((time.time() - start_time) * 1000)

        return {
            "suggestions": suggestions,
            "action_trace": self.action_trace,
            "execution_time_ms": execution_time_ms,
        }

# ---------------------------------------------------------------------------
# Convenience function for API layer
# ---------------------------------------------------------------------------

def run_agent(query: str, location: str = "Ocean Park 1") -> Dict[str, Any]:
    """
    Run the ReAct agent and return the result.
    This is the function that the API routes will call.
    """
    agent = ReActAgent()
    return agent.run(query, location)


# ---------------------------------------------------------------------------
# For testing / demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Quick demo
    result = run_agent("Giao nhanh", "Ocean Park 1")
    print(json.dumps(result, indent=2, ensure_ascii=False))
