from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.routes import router

from app.clients.database import PostgresClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    PostgresClient.connect()
    yield

def create_app() -> FastAPI:

    app = FastAPI(
        title="Bee",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.include_router(router)
    
    return app

app = create_app()