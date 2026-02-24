<div align="center">

# 🎓 VIDYA OS
### Sovereign On-Device AI Campus Intelligence Platform

[![AMD Slingshot 2025](https://img.shields.io/badge/AMD%20Slingshot-2025-ff0000?style=for-the-badge&logo=amd&logoColor=white)](https://www.amd.com)
[![Track](https://img.shields.io/badge/Track-Open%20Innovation-6366f1?style=for-the-badge)](.)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61dafb?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)

**The AI brain every Indian campus deserves — private, multilingual, and running entirely on AMD hardware.**

*No cloud. No API fees. No data leaving campus. Ever.*

[🧠 LEARN](#-learn--ai-tutor) · [⚙️ OPERATE](#️-operate--campus-os) · [🎨 CREATE](#-create--ai-app-builder) · [🚀 Quick Start](#-quick-start)

</div>

---

## 🎯 The Problem

4,000+ Indian colleges. 40 million students. Countless disconnected tools.

- Students waste hours on admin — forms, finding rooms, tracking schedules
- Cloud AI = expensive API costs + data sovereignty risk + fails offline
- Regional language learners are left behind by English-only tools
- Non-CS students can't build or customise AI tools for their clubs and events
- Campus data (energy, space, safety) is siloed and unactionable

**VIDYA OS solves this with a single, on-campus AI platform.**

---

## ✨ Three Pillars

### 🧠 LEARN — AI Tutor
> Multilingual, on-device academic coaching for every student

- **Streaming AI chat** powered by Llama 3.2 via Ollama
- **Voice input** in English, Hindi, Tamil, and Bengali (Web Speech API)
- **Instant quiz generation** from any topic discussed
- **Step-by-step explanations** with source attribution
- **Spaced repetition** — remembers what you struggled with

### ⚙️ OPERATE — Campus OS
> Real-time intelligence across your entire campus

- **Live KPI dashboard**: footfall, energy (kWh), AQI, space utilisation
- **WebSocket streaming** — data refreshes every 5 seconds
- **AI-generated alerts**: anomaly detection with plain-language remediation guidance
- **24-hour trend charts** for energy and footfall
- **Building-by-building** occupancy heatmap

### 🎨 CREATE — AI App Builder
> Let any student build and deploy AI tools — zero code required

- **3 ready templates**: FAQ Chatbot, Event Assistant, Feedback Collector
- **No-code form builder** — name it, configure it, publish it
- **Live preview** before publishing
- **Instant deploy** → shareable URL, live chat interface
- **LLM-powered** — every published app uses your campus AI

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              React PWA (Vite) · :5173                   │
│  LandingPage │ LearnPage │ OperatePage │ CreatePage      │
└──────────────────────────┬──────────────────────────────┘
                           │ REST / WebSocket
┌──────────────────────────▼──────────────────────────────┐
│              FastAPI Backend · :8000                     │
│  /api/learn/*  │  /api/operate/*  │  /api/create/*       │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│         AMD Hardware Layer (On-Premise)                  │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Ollama → Llama 3.2 + Whisper                   │    │
│  │  AMD Radeon GPU (ROCm) / Ryzen AI NPU            │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

**Tech Stack:**

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Recharts, React Router, Lucide |
| Backend | Python 3.10+, FastAPI, Uvicorn, WebSockets |
| AI Inference | Ollama (Llama 3.2), AMD ROCm / CUDA |
| Styling | Vanilla CSS, Space Grotesk + Inter fonts |

---

## 🚀 Quick Start

### Prerequisites
| Tool | Version | Install |
|------|---------|---------|
| Python | 3.10+ | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Ollama | Latest | [ollama.com](https://ollama.com) |

### 1. Pull AI Models
```bash
ollama pull llama3.2
```

### 2. Clone & Start Backend
```bash
git clone https://github.com/archittmittal/Slingshot
cd Slingshot
```

```powershell
# Windows (PowerShell)
.\start-backend.ps1
```

Or manually:
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Start Frontend
```powershell
# Windows
.\start-frontend.ps1
```
Or:
```bash
cd frontend
npm install
npm run dev
```

### 4. Open in Browser
```
http://localhost:5173
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check + model info |
| `POST` | `/api/learn/chat` | Streaming LLM chat (SSE) |
| `POST` | `/api/learn/quiz` | Generate MCQ quiz from topic |
| `GET` | `/api/operate/metrics` | Live campus snapshot |
| `GET` | `/api/operate/history` | 24-hour historical data |
| `WS` | `/ws/campus` | Live WebSocket feed (5s interval) |
| `GET` | `/api/create/templates` | List app templates |
| `POST` | `/api/create/apps` | Publish a new app |
| `GET` | `/api/create/apps` | List all published apps |
| `POST` | `/api/create/apps/{id}/chat` | Chat with a deployed app |

**Interactive API docs:** `http://localhost:8000/docs`

---

## 🔧 AMD Deployment

VIDYA OS is architected to run on **AMD hardware** with zero code changes:

| Dev (NVIDIA) | Production (AMD) |
|-------------|-----------------|
| Ollama with CUDA | Ollama with ROCm |
| `faster-whisper` CUDA | `faster-whisper` ROCm |
| Any CUDA GPU | AMD Radeon RX 7900 / EPYC |

**Enable AMD ROCm:**
```bash
# Linux — ROCm-enabled Ollama
OLLAMA_ROCm=1 ollama serve

# Or use the ROCm-specific Ollama build:
# https://ollama.com/download/linux#rocm
```

> Every inference call stays on campus — no cloud, no cost per token, no data exposure.

---

## 📁 Project Structure

```
Slingshot/
├── backend/
│   ├── main.py              # FastAPI app — all APIs in one file
│   ├── requirements.txt
│   └── .env.example         # Copy to .env and configure
├── frontend/
│   └── src/
│       ├── App.jsx           # Root layout, sidebar, routing
│       ├── App.css
│       ├── index.css         # Global design system
│       └── pages/
│           ├── LandingPage.jsx / .css   # Hero, stats, pillar overview
│           ├── LearnPage.jsx / .css     # AI tutor + voice + quiz
│           ├── OperatePage.jsx / .css   # Live campus dashboard
│           └── CreatePage.jsx / .css    # No-code app builder
├── start-backend.ps1        # One-click backend startup (Windows)
├── start-frontend.ps1       # One-click frontend startup (Windows)
└── README.md
```

---

## 🌍 Responsible AI

| Risk | Mitigation Built In |
|------|-------------------|
| Data privacy | Zero data leaves campus — no cloud API |
| Hallucinations | Source attribution on every AI response |
| Bias in feedback | Structured, rubric-based evaluation |
| Content safety | Llama Guard filter layer |
| Misuse of app builder | Admin approval flow for published apps |
| Offline access | Fully functional without internet |

---

## 🏆 Why This Wins — AMD Slingshot 2025

| Judging Criteria | VIDYA OS |
|----------------|---------|
| **Innovation** | First sovereign campus AI OS — not a chatbot wrapper |
| **AMD Hardware** | Every inference layer uses AMD silicon (ROCm + NPU) |
| **Impact** | 40M+ Indian college students; works offline |
| **Technical Depth** | Streaming LLM, WebSockets, RAG-ready, multi-agent |
| **Responsible AI** | Privacy-by-design, explainability, content filters |
| **Scalability** | One AMD server → entire campus; open-source → any college |

**Cross-track coverage:** GenAI (Track 1) + Education (Track 2) + Smart Cities (Track 8) + Social Good (Track 5) + Productivity (Track 3) + Cybersecurity (Track 6) → **Open Innovation (Track 9)**

---

## 👥 Team

Built for **AMD Slingshot 2025** — National Hackathon

---

<div align="center">

*Built with ❤️ for India's 40 million college students*

**VIDYA OS · AMD Slingshot 2025 · Open Innovation**

</div>