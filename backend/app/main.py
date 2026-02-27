from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

app = FastAPI(
    title="VIDYA OS 2.0 API",
    description="Sovereign Multi-Agent Campus Intelligence",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "VIDYA OS 2.0 Sovereign AI Engine Online"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine": settings.INFERENCE_ENGINE,
        "model": settings.MODEL_PATH
    }
