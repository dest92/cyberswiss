import uuid

import redis.asyncio as redis_async
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from app.api.deps import get_current_user
from app.core.config import settings
from app.core.docker_runner import EOF_MARKER
from app.models.user import User

router = APIRouter(tags=["jobs"])


@router.websocket("/ws/jobs/{job_id}/logs")
async def job_logs_ws(
    websocket: WebSocket,
    job_id: uuid.UUID,
    current_user: User | None = Depends(get_current_user),
) -> None:
    await websocket.accept()
    redis_client = redis_async.from_url(settings.redis_url)
    channel = f"job:{job_id}:logs"
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)
    try:
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            data = message["data"].decode("utf-8", errors="replace")
            if data == EOF_MARKER:
                break
            await websocket.send_text(data)
    except WebSocketDisconnect:
        pass
    finally:
        await pubsub.unsubscribe(channel)
        await redis_client.close()
