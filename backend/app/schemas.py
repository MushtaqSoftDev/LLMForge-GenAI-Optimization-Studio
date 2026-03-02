from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ──── Auth ────

class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=5, max_length=120)
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ──── Generation Parameters ────

class GenerationParams(BaseModel):
    max_tokens: int = Field(default=256, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)
    top_k: int = Field(default=50, ge=1, le=100)


# ──── Chat ────

class ChatRequest(BaseModel):
    session_id: int | None = None
    provider: str
    message: str
    params: GenerationParams = GenerationParams()


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    parameters: dict | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class SessionResponse(BaseModel):
    id: int
    title: str
    provider: str
    created_at: datetime
    messages: list[MessageResponse] = []

    model_config = {"from_attributes": True}


class ChatResponse(BaseModel):
    session_id: int
    reply: MessageResponse


# ──── Providers ────

class ProviderInfo(BaseModel):
    name: str
    label: str
    available: bool
