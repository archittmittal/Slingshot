from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.inference import inference_service

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    system_prompt: str = "You are VIDYA, a sovereign AI tutor."

@router.post("/chat")
async def chat(request: ChatRequest):
    async def token_generator():
        async for token in inference_service.stream_chat(
            request.prompt, 
            request.system_prompt
        ):
            yield token
            
    return StreamingResponse(token_generator(), media_type="text/plain")
