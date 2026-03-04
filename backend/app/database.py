from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import StaticPool

from app.config import settings

# Optional: no external DB — use in-memory SQLite (signup/login/chat all work; data resets on restart)
if settings.DISABLE_DB.strip().lower() in ("true", "1", "yes"):
    _db_url = "sqlite+aiosqlite:///:memory:"
    _connect_args = {}
    _poolclass = StaticPool
else:
    _db_url = settings.DATABASE_URL
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif _db_url.startswith("postgresql://") and "+asyncpg" not in _db_url:
        _db_url = _db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    _connect_args = {}
    _poolclass = None
    if settings.DATABASE_SSL.strip().lower() in ("true", "1", "yes"):
        _connect_args["ssl"] = True

engine = create_async_engine(
    _db_url,
    echo=False,
    connect_args=_connect_args,
    poolclass=_poolclass,
)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session
