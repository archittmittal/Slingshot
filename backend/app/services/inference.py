import torch
import asyncio
from typing import AsyncGenerator
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread
from app.core.config import settings

class InferenceService:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        
    async def load_model(self):
        """Lazy load the transformers model."""
        if self.model is None:
            self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_PATH)
            self.model = AutoModelForCausalLM.from_pretrained(
                settings.MODEL_PATH,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True
            )
            
    async def stream_chat(self, prompt: str, system_prompt: str = "") -> AsyncGenerator[str, None]:
        await self.load_model()
        
        full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{prompt}\n<|assistant|>\n"
        inputs = self.tokenizer(full_prompt, return_tensors="pt").to(self.model.device)
        
        streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        generation_kwargs = dict(
            **inputs,
            streamer=streamer,
            max_new_tokens=2048,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Run generation in a separate thread to allow async streaming
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        for new_text in streamer:
            yield new_text
            await asyncio.sleep(0) # Yield control

inference_service = InferenceService()
