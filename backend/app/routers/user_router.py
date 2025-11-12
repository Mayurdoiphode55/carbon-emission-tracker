from fastapi import APIRouter, HTTPException
from app.db import database
from app.models import User
from sqlalchemy import select, insert
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

# request schema
class UserIn(BaseModel):
    email: str
    full_name: str | None = None

@router.get("/")
async def get_users():
    query = select(User)
    rows = await database.fetch_all(query)
    return rows

@router.post("/")
async def create_user(user: UserIn):
    query = insert(User).values(email=user.email, full_name=user.full_name)
    try:
        await database.execute(query)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
