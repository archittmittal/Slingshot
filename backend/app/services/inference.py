import asyncio
import json
import httpx
from typing import AsyncGenerator
from app.core.config import settings


SYSTEM_PROMPTS = {
    "learn": (
        "You are VIDYA, a sovereign AI tutor built for Indian campuses. "
        "Be concise, friendly, and explain step-by-step. "
        "Support Hinglish if the user mixes Hindi and English."
    ),
    "operate": (
        "You are VIDYA Campus Intel. Analyse campus metrics and give "
        "plain-language alerts with actionable recommendations."
    ),
    "create": (
        "You are VIDYA Builder. Help users design campus AI tools. "
        "Be helpful and suggest improvements to their app ideas."
    ),
}


class InferenceService:
    """
    Sovereign SLM Inference via HuggingFace Inference API.
    No local model download — uses HF cloud, zero device storage.
    Falls back gracefully if token is not set.
    """

    def __init__(self):
        self.model_url = (
            f"https://api-inference.huggingface.co/models/{settings.HF_MODEL_ID}"
        )
        self.chat_url = (
            f"https://api-inference.huggingface.co/v1/chat/completions"
        )
        self.headers = {
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
            "Content-Type": "application/json",
        }

    async def stream_chat(
        self,
        prompt: str,
        system_prompt: str = "",
        mode: str = "learn",
    ) -> AsyncGenerator[str, None]:
        if not system_prompt:
            system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["learn"])

        payload = {
            "model": settings.HF_MODEL_ID,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 1024,
            "temperature": 0.7,
            "stream": True,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST",
                    self.chat_url,
                    headers=self.headers,
                    json=payload,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data = line[6:]
                            if data == "[DONE]":
                                break
                            try:
                                chunk = json.loads(data)
                                delta = chunk["choices"][0]["delta"].get("content", "")
                                if delta:
                                    yield delta
                            except (json.JSONDecodeError, KeyError):
                                continue
        except Exception as e:
            yield f"[VIDYA Error: {str(e)}]"

    async def simple_chat(self, prompt: str, mode: str = "learn") -> str:
        """Non-streaming chat for quiz generation and single-shot tasks."""
        result = []
        async for token in self.stream_chat(prompt, mode=mode):
            result.append(token)
        return "".join(result)


inference_service = InferenceService()
