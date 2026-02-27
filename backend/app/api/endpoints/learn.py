from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.services.inference import inference_service

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = ""
    mode: Optional[str] = "learn"


class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5


@router.post("/chat")
async def chat(request: ChatRequest):
    """Stream a response from the sovereign SLM (HF Inference API)."""
    async def token_generator():
        async for token in inference_service.stream_chat(
            request.prompt,
            system_prompt=request.system_prompt,
            mode=request.mode,
        ):
            yield token

    return StreamingResponse(token_generator(), media_type="text/plain")


@router.post("/quiz")
async def generate_quiz(request: QuizRequest):
    """Generate MCQ quiz from a topic."""
    prompt = (
        f"Generate {request.num_questions} multiple choice questions about '{request.topic}'. "
        "Format as JSON array: [{question, options:[A,B,C,D], answer}]. Return only JSON."
    )
    result = await inference_service.simple_chat(prompt, mode="learn")
    return {"quiz": result, "topic": request.topic}
