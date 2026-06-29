from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    auth,
    engagements,
    jobs,
    notes,
    pipelines,
    scopes,
    targets,
    tools,
    ws_logs,
)
from app.core.config import settings

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(engagements.router)
app.include_router(scopes.router)
app.include_router(notes.router)
app.include_router(tools.router)
app.include_router(jobs.router)
app.include_router(targets.router)
app.include_router(pipelines.catalog_router)
app.include_router(pipelines.router)
app.include_router(ws_logs.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
