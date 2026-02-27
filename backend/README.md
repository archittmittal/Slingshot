---
title: VIDYA OS 2.0 Sovereign AI Backend
emoji: 🎓
colorFrom: purple
colorTo: emerald
sdk: docker
pinned: true
license: mit
short_description: Bharat-First Multi-Agent Campus Intelligence API
---

# VIDYA OS 2.0 — Sovereign AI Backend

FastAPI backend powering the VIDYA OS platform.

## Environment Variables (set in Spaces → Settings → Variables)

| Variable | Description |
|----------|-------------|
| `HF_API_TOKEN` | Your HuggingFace API token (read access) |
| `HF_MODEL_ID` | Model to use (default: `microsoft/Phi-3.5-mini-instruct`) |
| `QDRANT_URL` | Qdrant Cloud cluster URL |
| `QDRANT_API_KEY` | Qdrant Cloud API key |
| `FRONTEND_URL` | Your Vercel frontend URL (for CORS) |

## API Docs

Visit `https://<your-space>.hf.space/docs` for interactive Swagger UI.
