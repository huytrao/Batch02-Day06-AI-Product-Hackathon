from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from api.agent import ReActAgent
from api.tool_runners import execute_tool

router = APIRouter()
agent = ReActAgent()

class QueryRequest(BaseModel):
    query: str
    location: str

class FeedbackRequest(BaseModel):
    query: str
    suggestion_id: int
    rating: int
    text: Optional[str] = ""

@router.post("/query")
async def process_query(req: QueryRequest):
    try:
        result = agent.run(req.query, req.location)
        return result
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
