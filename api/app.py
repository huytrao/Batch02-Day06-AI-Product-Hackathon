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
from api import db
from api.version import __version__

app = FastAPI(
    title="Ocean Park 1 Eats — API",
    description="ReAct-agent-powered restaurant recommendation system for Ocean Park 1 residents.",
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
# Mount routes
# ---------------------------------------------------------------------------
app.include_router(router)


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
