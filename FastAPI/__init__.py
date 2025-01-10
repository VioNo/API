from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import engine, metadata
from .main import router

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)
