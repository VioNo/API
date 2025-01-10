from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from models import users
from schemas import UserCreate, User

def get_users(db: Session):
    query = select([users])
    result = db.execute(query)
    return result.fetchall()

def get_user(db: Session, user_id: int):
    query = select([users]).where(users.c.id == user_id)
    result = db.execute(query)
    return result.fetchone()

def create_user(db: Session, user: UserCreate):
    query = insert(users).values(name=user.name, email=user.email)
    db.execute(query)
    db.commit()
    return {"name": user.name, "email": user.email}

def update_user(db: Session, user_id: int, user: UserCreate):
    query = update(users).where(users.c.id == user_id).values(name=user.name, email=user.email)
    db.execute(query)
    db.commit()
    return {"id": user_id, "name": user.name, "email": user.email}

def delete_user(db: Session, user_id: int):
    query = delete(users).where(users.c.id == user_id)
    db.execute(query)
    db.commit()
    return {"id": user_id}
