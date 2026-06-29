from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.tools import registry

router = APIRouter(prefix="/api/tools", tags=["tools"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[str])
async def list_tools() -> list[str]:
    return registry.list_tools()
