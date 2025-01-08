from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import User
from .schemas import UserCreate, UserUpdate
from .database import SessionDep

async def get_user(db: SessionDep, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def get_users(db: SessionDep, skip: int = 0, limit: int = 10):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

async def create_user(db: SessionDep, user: UserCreate):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: SessionDep, user_id: int, user: UserUpdate):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        await db.commit()
        await db.refresh(db_user)
    return db_user

async def delete_user(db: SessionDep, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    db_user = result.scalar_one_or_none()
    if db_user:
        await db.delete(db_user)
        await db.commit()
    return db_user
