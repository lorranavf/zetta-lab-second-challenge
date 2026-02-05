from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.database import PostgresClient
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    PostgresClient.connect()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Bee", version="1.0.0", lifespan=lifespan)

    app.include_router(router)

    return app


app = create_app()
