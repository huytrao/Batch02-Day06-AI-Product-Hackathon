import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from api.agent import ReActAgent
from api.tool_runners import execute_tool

router = APIRouter()
agent = ReActAgent()

class QueryRequest(BaseModel):
    query: str
    location: str = "Ocean Park 1"

class FeedbackRequest(BaseModel):
    query: str
    suggestion_id: int
    rating: int
    text: Optional[str] = ""

@router.post("/query")
async def process_query(req: QueryRequest):
    try:
        start = time.time()
        result = agent.run(req.query, req.location)
        elapsed_ms = int((time.time() - start) * 1000)

        # The LLM agent returns {query, action_trace, final_answer} or {query, action_trace, error}
        # The frontend expects {suggestions, action_trace, execution_time_ms}
        action_trace = result.get("action_trace", [])

        final_answer = result.get("final_answer", {})

        # final_answer may contain suggestions directly or be a dict with a suggestions key
        if isinstance(final_answer, dict):
            suggestions = final_answer.get("suggestions", [])
        elif isinstance(final_answer, list):
            suggestions = final_answer
        else:
            suggestions = []

        # Fallback: if no suggestions from final_answer, extract from action_trace
        # (e.g. when agent hit max steps or returned error)
        if not suggestions:
            for step in action_trace:
                if step.get("tool") == "query_restaurants" and isinstance(step.get("result"), list) and step["result"]:
                    restaurants = step["result"]
                    for r in restaurants:
                        if r.get("is_open", True) and r.get("confidence", 0) >= 0.5:
                            suggestions.append({
                                "id": r.get("id"),
                                "name": r.get("name"),
                                "eta": r.get("predicted_eta"),
                                "confidence": r.get("confidence"),
                                "reason": f"Gợi ý từ dữ liệu tìm kiếm (rating: {r.get('rating', 'N/A')}, giá TB: {r.get('avg_price', 'N/A')}đ)."
                            })
                    break

        return {
            "suggestions": suggestions,
            "action_trace": action_trace,
            "execution_time_ms": elapsed_ms,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    try:
        result = execute_tool("record_feedback", {
            "query": req.query,
            "suggestion_id": req.suggestion_id,
            "user_rating": req.rating,
            "feedback_text": req.text
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "ok"}
