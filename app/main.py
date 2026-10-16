from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import initialize_database
from app.routes.base import router


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Student Records API",
    description="Student CRUD API with an optional local Ollama query extension.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}