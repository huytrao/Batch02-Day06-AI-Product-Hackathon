#!/usr/bin/env python3
"""
FastAPI server for Ocean Park 1 Eats prototype.

Usage:
    python api/app.py                          # development (reload on)
    uvicorn api.app:app --host 0.0.0.0 --port 8000   # production-style
"""

import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path so `from api import ...` works
# when running `python api/app.py` from any working directory
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from api.feedback_routes import create_feedback_router
from api.request_logger import install_request_logger
from api.feedback_db import init_feedback_db
from api import db
from api.version import __version__

app = FastAPI(
    title="Ocean Park 1 Gợi Ý — API",
    description="Trợ lý gợi ý quán ăn dùng ReAct agent cho cư dân Ocean Park 1.",
    version=__version__,
)

# ---------------------------------------------------------------------------
# CORS — allow frontend access from any origin during development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request/response evidence logging (PII-scrubbed) — Member E
# ---------------------------------------------------------------------------
install_request_logger(app)

# ---------------------------------------------------------------------------
# Mount routes
#   - api.routes:        /api/query, /api/health          (Members B + C)
#   - feedback router:   /api/feedback, /api/analytics,
#                        /api/partner-stats               (Member E)
# ---------------------------------------------------------------------------
app.include_router(router)
app.include_router(create_feedback_router(), prefix="/api")


# ---------------------------------------------------------------------------
# Startup event: verify DB connectivity
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup():
    try:
        count = db.count_restaurants()
        print(f"[startup] DB connected: {count} restaurants found.")
    except Exception as e:
        print(f"[startup] WARNING: Could not connect to DB: {e}")
        print("Make sure to run `python scripts/generate_seed_data.py` first.")
    try:
        init_feedback_db()
        print("[startup] Feedback DB initialized.")
    except Exception as e:
        print(f"[startup] WARNING: Could not initialize feedback DB: {e}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
