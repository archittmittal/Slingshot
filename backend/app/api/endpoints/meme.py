from fastapi import APIRouter
import random
from pydantic import BaseModel
from typing import List, Optional
from app.services.inference import inference_service

router = APIRouter()

CAMPUS_SITUATIONS = [
    "When the library is full during finals week",
    "Trying to find a charging port in the lecture hall",
    "Eating at the mess after a 3-hour lab",
    "When the professor says 'Last 5 minutes' and you haven't started Q1",
    "Running to class at 8:59 AM",
    "When the WiFi works for exactly 2 seconds",
    "Senior giving 'advice' that sounds like a side quest",
    "The 1% battery struggle during a presentation"
]

class MemeGenerateRequest(BaseModel):
    situation: str
    language: Optional[str] = "Hinglish"

@router.get("/trending")
async def get_trending():
    return {"situations": random.sample(CAMPUS_SITUATIONS, 4)}

@router.post("/generate")
async def generate_meme(request: MemeGenerateRequest):
    prompt = (
        f"Generate a short, hilarious meme caption for this campus situation: '{request.situation}'. "
        f"Language: {request.language}. Make it relatable and witty. "
        "Return exactly two parts: [TOP TEXT] and [BOTTOM TEXT] as a JSON object."
    )
    
    result = await inference_service.simple_chat(prompt, mode="builder")
    # For now, return mock if LLM is slow or for stable demo
    return {
        "id": random.randint(1000, 9999),
        "situation": request.situation,
        "caption": result or {"top": "AI thinking...", "bottom": "Memes loading..."}
    }
