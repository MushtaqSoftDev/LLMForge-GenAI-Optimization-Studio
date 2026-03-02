from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth_router, chat_router, provider_router
from app.routers import finetune_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="LLM Experiment Lab", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["Chat"])
app.include_router(provider_router.router, prefix="/api/providers", tags=["Providers"])
app.include_router(finetune_router.router, prefix="/api/finetune", tags=["Fine-tuning"])


@app.get("/health")
async def health():
    return {"status": "ok"}
