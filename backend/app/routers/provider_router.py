from fastapi import APIRouter

from app.schemas import ProviderInfo
from app.services.chat_service import get_all_providers

router = APIRouter()


@router.get("/", response_model=list[ProviderInfo])
async def list_providers():
    providers = get_all_providers()
    return [
        ProviderInfo(name=p.name, label=p.label, available=p.is_available())
        for p in providers
    ]
