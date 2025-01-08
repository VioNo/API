from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, SessionDep
from .crud import get_user, get_users, create_user, update_user, delete_user
from .schemas import UserCreate, UserUpdate, UserInDB

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

@app.post("/users/", response_model=UserInDB)
async def create_user_endpoint(user: UserCreate, db: SessionDep = Depends()):
    return await create_user(db, user)

@app.get("/users/{user_id}", response_model=UserInDB)
async def read_user_endpoint(user_id: int, db: SessionDep = Depends()):
    return await get_user(db, user_id)

@app.get("/users/", response_model=list[UserInDB])
async def read_users_endpoint(skip: int = 0, limit: int = 10, db: SessionDep = Depends()):
    return await get_users(db, skip, limit)

@app.put("/users/{user_id}", response_model=UserInDB)
async def update_user_endpoint(user_id: int, user: UserUpdate, db: SessionDep = Depends()):
    return await update_user(db, user_id, user)

@app.delete("/users/{user_id}", response_model=UserInDB)
async def delete_user_endpoint(user_id: int, db: SessionDep = Depends()):
    return await delete_user(db, user_id)
