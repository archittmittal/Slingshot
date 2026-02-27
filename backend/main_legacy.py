import os
import json
import asyncio
import random
import httpx
from datetime import datetime
from typing import Optional, AsyncGenerator

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

app = FastAPI(title="VIDYA OS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
#  MODELS
# ─────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    language: Optional[str] = "English"

class AppTemplate(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    components: list[dict]

class CreatedApp(BaseModel):
    id: str
    name: str
    template_id: str
    config: dict
    created_at: str

# In-memory store for created apps
created_apps: dict[str, CreatedApp] = {}

# ─────────────────────────────────────────
#  HEALTH
# ─────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": LLM_MODEL, "timestamp": datetime.now().isoformat()}

# ─────────────────────────────────────────
#  LEARN — AI TUTOR
# ─────────────────────────────────────────

SYSTEM_PROMPTS = {
    "English": (
        "You are VIDYA, a friendly and brilliant AI tutor for college students. "
        "Always explain concepts step by step with examples. "
        "When answering, structure your response clearly with numbered steps if needed. "
        "Always cite which subject or topic area your answer comes from. "
        "Keep answers concise but complete."
    ),
    "Hindi": (
        "Aap VIDYA hain, ek dost aur brilliant AI tutor jo college students ki madad karte hain. "
        "Hamesha concepts ko step-by-step examples ke saath samjhaen. "
        "Apne jawaab ko clear karein aur agar zaruri ho to numbered steps use karein. "
        "Jawaab Hindi mein dein lekin technical terms English mein rakh sakte hain."
    ),
    "Tamil": (
        "Neenga VIDYA, oru nalla AI tutor. College students ukku udhavanum. "
        "Concepts step-by-step explain pannunga. Tamil la answer panuga."
    ),
    "Bengali": (
        "Aap VIDYA, ekjon bondhu ebong brilliant AI tutor college students ke sাহায্য করার জন্য। "
        "সর্বদা step-by-step examples দিয়ে concepts বোঝান। Bengali তে উত্তর দিন।"
    ),
}

async def stream_ollama(messages: list[dict], language: str) -> AsyncGenerator[str, None]:
    system_prompt = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["English"])
    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream": True,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        async with client.stream("POST", f"{OLLAMA_BASE_URL}/api/chat", json=payload) as resp:
            async for line in resp.aiter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        token = data.get("message", {}).get("content", "")
                        if token:
                            yield token
                    except json.JSONDecodeError:
                        continue

@app.post("/api/learn/chat")
async def chat(req: ChatRequest):
    messages = [{"role": m.role, "content": m.content} for m in req.messages]

    async def generator():
        async for token in stream_ollama(messages, req.language):
            yield token

    return StreamingResponse(generator(), media_type="text/plain")

@app.post("/api/learn/quiz")
async def generate_quiz(req: ChatRequest):
    """Generate a short quiz based on the conversation topic."""
    topic = req.messages[-1].content if req.messages else "general knowledge"
    quiz_prompt = [
        {
            "role": "user",
            "content": (
                f"Based on this topic: '{topic}', generate exactly 3 multiple-choice questions. "
                "Return ONLY valid JSON in this format: "
                '[{"q":"question","options":["A","B","C","D"],"answer":"A"}]. '
                "No markdown, no explanation, just raw JSON array."
            ),
        }
    ]
    full_response = ""
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={"model": LLM_MODEL, "messages": quiz_prompt, "stream": False},
        )
        full_response = resp.json().get("message", {}).get("content", "[]")
    # Extract JSON from response
    start = full_response.find("[")
    end = full_response.rfind("]") + 1
    try:
        quiz = json.loads(full_response[start:end])
    except Exception:
        quiz = []
    return {"quiz": quiz}

# ─────────────────────────────────────────
#  OPERATE — CAMPUS DASHBOARD
# ─────────────────────────────────────────

def generate_campus_snapshot():
    """Generate a realistic campus metrics snapshot."""
    hour = datetime.now().hour
    # Footfall is higher during class hours
    peak = 1.0 if 9 <= hour <= 17 else 0.3
    energy_base = 420 if peak == 1.0 else 180

    buildings = [
        {"id": "main", "name": "Main Block", "occupancy": int(random.uniform(60, 95) * peak), "energy": round(random.uniform(80, 120) * peak, 1)},
        {"id": "cs_lab", "name": "CS Lab", "occupancy": int(random.uniform(50, 90) * peak), "energy": round(random.uniform(60, 90) * peak, 1)},
        {"id": "library", "name": "Library", "occupancy": int(random.uniform(40, 80) * peak), "energy": round(random.uniform(30, 50) * peak, 1)},
        {"id": "hostel_a", "name": "Hostel A", "occupancy": int(random.uniform(30, 70)), "energy": round(random.uniform(40, 70), 1)},
        {"id": "hostel_b", "name": "Hostel B", "occupancy": int(random.uniform(30, 70)), "energy": round(random.uniform(40, 70), 1)},
        {"id": "canteen", "name": "Canteen", "occupancy": int(random.uniform(20, 95) if hour in [8,9,13,14,19,20] else random.uniform(5, 30)), "energy": round(random.uniform(25, 60), 1)},
        {"id": "sports", "name": "Sports Complex", "occupancy": int(random.uniform(10, 60) if hour >= 16 else random.uniform(5, 20)), "energy": round(random.uniform(15, 40), 1)},
        {"id": "admin", "name": "Admin Block", "occupancy": int(random.uniform(40, 80) * peak), "energy": round(random.uniform(20, 45) * peak, 1)},
    ]

    alerts = []
    total_energy = sum(b["energy"] for b in buildings)
    if total_energy > 450:
        alerts.append({"severity": "warning", "location": "Campus-wide", "message": f"Energy consumption at {total_energy:.0f} kWh — 18% above average. Consider turning off unused AC units.", "time": datetime.now().strftime("%H:%M")})
    for b in buildings:
        if b["occupancy"] > 88:
            alerts.append({"severity": "info", "location": b["name"], "message": f"High occupancy ({b['occupancy']}%). Consider opening overflow space.", "time": datetime.now().strftime("%H:%M")})

    # Random maintenance alert occasionally
    if random.random() < 0.15:
        labs = ["CS Lab 3", "Physics Lab", "Chemistry Lab", "E&C Lab"]
        alerts.append({"severity": "critical", "location": random.choice(labs), "message": "Temperature sensor reading abnormal (32°C). HVAC check recommended.", "time": datetime.now().strftime("%H:%M")})

    return {
        "timestamp": datetime.now().isoformat(),
        "kpis": {
            "total_footfall": sum(b["occupancy"] for b in buildings),
            "total_energy_kwh": round(total_energy, 1),
            "active_spaces": len([b for b in buildings if b["occupancy"] > 20]),
            "air_quality_aqi": random.randint(32, 78),
        },
        "buildings": buildings,
        "alerts": alerts,
    }

@app.get("/api/operate/metrics")
async def get_metrics():
    return generate_campus_snapshot()

@app.get("/api/operate/history")
async def get_history():
    """Return 24-hour historical data for charts."""
    history = []
    for i in range(24):
        peak = 1.0 if 9 <= i <= 17 else 0.4
        history.append({
            "hour": f"{i:02d}:00",
            "footfall": int(random.uniform(200, 800) * peak),
            "energy": round(random.uniform(150, 500) * peak, 1),
            "aqi": random.randint(25, 85),
        })
    return {"history": history}

@app.websocket("/ws/campus")
async def campus_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = generate_campus_snapshot()
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass

# ─────────────────────────────────────────
#  CREATE — NO-CODE APP BUILDER
# ─────────────────────────────────────────

APP_TEMPLATES = [
    {
        "id": "faq_bot",
        "name": "FAQ Chatbot",
        "description": "Answer common questions about your club, event, or department automatically.",
        "icon": "💬",
        "components": [
            {"type": "text_input", "label": "Bot Name", "placeholder": "e.g. TechFest Help Bot"},
            {"type": "textarea", "label": "FAQ Content", "placeholder": "Q: What time does fest start?\nA: 9 AM sharp!\n\nQ: Is registration free?\nA: Yes, completely free!"},
            {"type": "color_picker", "label": "Theme Color", "default": "#6366f1"},
            {"type": "select", "label": "Language", "options": ["English", "Hindi", "Tamil", "Bengali"]},
        ],
    },
    {
        "id": "event_bot",
        "name": "Event Assistant",
        "description": "Help attendees navigate your event — schedule, venues, speakers, and more.",
        "icon": "🎉",
        "components": [
            {"type": "text_input", "label": "Event Name", "placeholder": "e.g. TechFest 2025"},
            {"type": "textarea", "label": "Event Schedule", "placeholder": "10:00 - Opening Ceremony (Main Hall)\n11:00 - Hackathon Kickoff (Lab 2)"},
            {"type": "text_input", "label": "Contact Email", "placeholder": "organizer@college.edu"},
            {"type": "color_picker", "label": "Brand Color", "default": "#f59e0b"},
        ],
    },
    {
        "id": "survey_bot",
        "name": "Feedback Collector",
        "description": "Collect structured feedback from students or event attendees conversationally.",
        "icon": "📋",
        "components": [
            {"type": "text_input", "label": "Survey Title", "placeholder": "e.g. Workshop Feedback"},
            {"type": "textarea", "label": "Questions (one per line)", "placeholder": "How would you rate the session? (1-5)\nWhat could be improved?\nWould you attend again?"},
            {"type": "select", "label": "Language", "options": ["English", "Hindi", "Tamil", "Bengali"]},
            {"type": "color_picker", "label": "Theme Color", "default": "#10b981"},
        ],
    },
]

@app.get("/api/create/templates")
async def get_templates():
    return {"templates": APP_TEMPLATES}

@app.post("/api/create/apps")
async def create_app(payload: dict):
    app_id = f"app_{random.randint(10000, 99999)}"
    new_app = {
        "id": app_id,
        "name": payload.get("name", "My App"),
        "template_id": payload.get("template_id"),
        "config": payload.get("config", {}),
        "created_at": datetime.now().isoformat(),
        "share_url": f"http://localhost:5173/app/{app_id}",
    }
    created_apps[app_id] = new_app
    return new_app

@app.get("/api/create/apps")
async def list_apps():
    return {"apps": list(created_apps.values())}

@app.post("/api/create/apps/{app_id}/chat")
async def app_chat(app_id: str, req: ChatRequest):
    """Execute a deployed app — answer questions using the app's config as context."""
    app_data = created_apps.get(app_id)
    if not app_data:
        return {"error": "App not found"}

    config = app_data.get("config", {})
    context = "\n".join([f"{k}: {v}" for k, v in config.items()])
    system = f"You are a helpful assistant for this app. Here is the app context:\n{context}\n\nAnswer questions based only on this context. Be concise."

    messages = [{"role": "system", "content": system}] + [
        {"role": m.role, "content": m.content} for m in req.messages
    ]

    async def generator():
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST",
                f"{OLLAMA_BASE_URL}/api/chat",
                json={"model": LLM_MODEL, "messages": messages, "stream": True},
            ) as resp:
                async for line in resp.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            token = data.get("message", {}).get("content", "")
                            if token:
                                yield token
                        except json.JSONDecodeError:
                            continue

    return StreamingResponse(generator(), media_type="text/plain")
