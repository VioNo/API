from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import get_session
from src.models import User

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.on_event("startup")
async def startup():
    pass

@app.on_event("shutdown")
async def shutdown():
    pass

@app.get("/users/")
def read_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    query = session.query(User).offset(skip).limit(limit)
    result = query.all()
    return result
