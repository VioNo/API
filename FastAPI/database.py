from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import declarative_base
from .config import POSTGRES_DATABASE_URL

engine = create_async_engine(POSTGRES_DATABASE_URL, echo=True)

async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]
Base = declarative_base()