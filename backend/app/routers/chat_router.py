from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.auth import get_current_user
from app.database import get_db
from app.models import ChatMessage, ChatSession, User
from app.schemas import ChatRequest, ChatResponse, MessageResponse, SessionResponse
from app.services.chat_service import generate_reply
from app.utils.provider_errors import to_user_friendly

router = APIRouter()


@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user.id)
        .options(selectinload(ChatSession.messages))
        .order_by(ChatSession.created_at.desc())
    )
    return result.scalars().all()


@router.get("/sessions/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id, ChatSession.user_id == user.id)
        .options(selectinload(ChatSession.messages))
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.post("/send", response_model=ChatResponse)
async def send_message(
    body: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    prior_messages: list[dict] = []

    if body.session_id:
        result = await db.execute(
            select(ChatSession)
            .where(ChatSession.id == body.session_id, ChatSession.user_id == user.id)
            .options(selectinload(ChatSession.messages))
        )
        session = result.scalar_one_or_none()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        prior_messages = [
            {"role": m.role, "content": m.content} for m in session.messages
        ]
    else:
        session = ChatSession(
            user_id=user.id,
            provider=body.provider,
            title=body.message[:80],
        )
        db.add(session)
        await db.flush()

    params_dict = body.params.model_dump()

    user_msg = ChatMessage(
        session_id=session.id,
        role="user",
        content=body.message,
        parameters=params_dict,
    )
    db.add(user_msg)
    await db.flush()

    history = prior_messages + [{"role": "user", "content": body.message}]

    try:
        reply_text = await generate_reply(body.provider, history, body.params)
    except Exception as exc:
        friendly = to_user_friendly(exc, body.provider)
        raise HTTPException(status_code=422, detail=friendly)

    assistant_msg = ChatMessage(
        session_id=session.id,
        role="assistant",
        content=reply_text,
        parameters=params_dict,
    )
    db.add(assistant_msg)
    await db.commit()
    await db.refresh(assistant_msg)

    return ChatResponse(
        session_id=session.id,
        reply=MessageResponse.model_validate(assistant_msg),
    )


@router.delete("/sessions/{session_id}", status_code=204)
async def delete_session(
    session_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ChatSession).where(
            ChatSession.id == session_id, ChatSession.user_id == user.id
        )
    )
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    await db.delete(session)
    await db.commit()
