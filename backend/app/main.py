from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="VIDYA OS 2.0 API",
    description="Sovereign Multi-Agent Campus Intelligence — Bharat-First, Global Standard",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow Vercel frontend and local dev
origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if settings.FRONTEND_URL != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "VIDYA OS 2.0 Sovereign AI Engine Online",
        "model": settings.HF_MODEL_ID,
        "status": "operational"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine": "HuggingFace Inference API",
        "model": settings.HF_MODEL_ID,
        "version": "2.0.0"
    }
