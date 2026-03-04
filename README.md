# LLMForge - GenAI Optimization Lab

A full-stack platform for experimenting with Large Language Models. Adjust inference parameters (temperature, top_p, top_k, max_tokens) in real time and compare results across multiple providers.

## Features

- **Login / Signup** with JWT authentication
- **Prompt Engineering** — interactive chatbot with adjustable generation parameters
- **Multi-provider** — DeepSeek, Groq, OpenAI (ChatGPT), Gemini, and a free HuggingFace local model (CPU)
- **Internationalization (i18n)** — English, Spanish, Catalan, German, French,,,,etc
- **PostgreSQL** for users, chat history, and parameter snapshots
- **Docker & Kubernetes** ready

## Architecture

| Layer | Tech |
|-------|------|
| Frontend | Vue 3, Vue Router, Pinia, vue-i18n, Vite |
| Backend | Python, FastAPI, SQLAlchemy (async), asyncpg |
| Database | PostgreSQL 16 |
| LLM Providers | OpenAI SDK (DeepSeek, Groq, ChatGPT), google-generativeai, transformers |
| DevOps | Docker, Docker Compose, Kubernetes |

## Quick Start

### 1. Clone and configure

```bash
cp .env.example .env
# edit .env — add your API keys (optional; HuggingFace local works without any key)
```

### 2. Run everything (Docker Compose)

One command runs frontend, backend, and PostgreSQL:

```bash
docker compose up --build
```

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000/docs
- **PostgreSQL:** localhost:5432

**CPU (default):** Fast build (~3–5 min). Fine-tuning uses full fine-tuning.

**GPU + LoRA:** Enable PEFT/LoRA when you have a GPU:

```bash
TORCH_GPU=1 docker compose build --no-cache backend && docker compose up -d
```

### 3. Run locally (without Docker)

For development with hot reload — run backend and frontend in separate terminals:

```bash
# Terminal 1 - Backend
cd backend && python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt && uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend && npm install && npm run dev
```

Requires PostgreSQL running (e.g. `docker compose up postgres -d`).


## Providers

| Provider | Requires API Key | Free Tier |
|----------|-----------------|-----------|
| HuggingFace Local | No | Always free (runs on your CPU) |
| Groq | Yes | Generous free tier |
| DeepSeek | Yes | Free credits |
| OpenAI (ChatGPT) | Yes | Paid |
| Gemini | Yes | Free tier available |

If all API keys are exhausted or missing, the HuggingFace local model (default: `google/flan-t5-small`, FLAN-T5) is always available.

## Parameters

| Parameter | Description | Range |
|-----------|-------------|-------|
| `temperature` | Controls randomness — higher = more creative | 0.0 – 2.0 |
| `max_tokens` | Maximum number of tokens to generate | 1 – 4096 |
| `top_p` | Nucleus sampling — cumulative probability cutoff | 0.0 – 1.0 |
| `top_k` | Consider only the top-k most likely tokens | 1 – 100 |

## Roadmap

- [x] Prompt Engineering module
- [x] Fine-tuning module (Full / LoRA; LoRA when GPU available)
- [ ] Reinforcement Learning module


## License

MIT




