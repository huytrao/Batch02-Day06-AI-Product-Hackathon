import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from codebase root
_CODEBASE_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_CODEBASE_ROOT / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="Hackathon API", description="AI Agent API for Restaurant Suggestions")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for the hackathon prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.app:app", host="0.0.0.0", port=8000, reload=True)