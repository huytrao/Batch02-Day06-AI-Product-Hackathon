"""
API route handlers for Ocean Park 1 Eats.

Endpoints:
- POST /api/query        Run ReAct agent against a user query
- POST /api/feedback     Submit feedback on a suggestion
- GET  /api/health       Health check / DB verification
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Any

from . import agent as agent_module
from . import db
from .version import __version__

router = APIRouter(prefix="/api")

# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="User query text")
    location: str = Field(default="Ocean Park 1", max_length=200, description="Delivery location")


class SuggestionResponse(BaseModel):
    id: int
    name: str
    vendor: str
    predicted_eta: int
    confidence: float
    evidence_links: List[str]
    cuisine: Optional[str] = None
    tags: Optional[List[str]] = None


class ActionTraceStep(BaseModel):
    step: int
    type: str  # think | action
    thought: Optional[str] = None
    tool: Optional[str] = None
    params: Optional[Any] = None
    result: Optional[Any] = None


class QueryResponse(BaseModel):
    suggestions: List[SuggestionResponse]
    action_trace: List[ActionTraceStep]
    execution_time_ms: int


class FeedbackRequest(BaseModel):
    query_text: str = Field(..., min_length=1, max_length=1000)
    suggestion_id: int
    rating: int = Field(..., ge=1, le=5)
    feedback_text: str = Field(default="", max_length=2000)


class FeedbackResponse(BaseModel):
    status: str
    feedback_id: int


class HealthResponse(BaseModel):
    status: str
    version: str
    database_restaurants_count: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Accept a user query and location, run the ReAct agent,
    and return ranked suggestions with an action trace.
    """
    try:
        result = agent_module.run_agent(
            query=request.query,
            location=request.location,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@router.post("/feedback", response_model=FeedbackResponse)
async def handle_feedback(request: FeedbackRequest):
    """
    Accept user feedback on a suggestion.
    Stores rating and optional text feedback.
    """
    try:
        feedback_id = db.save_feedback(
            query_text=request.query_text,
            suggestion_id=request.suggestion_id,
            rating=request.rating,
            feedback_text=request.feedback_text,
        )
        return FeedbackResponse(status="ok", feedback_id=feedback_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check — verifies DB connection and returns version info."""
    try:
        count = db.count_restaurants()
        return HealthResponse(
            status="ok",
            version=__version__,
            database_restaurants_count=count,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
