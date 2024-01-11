from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


class LoginRequest(BaseModel):
    username: str
    password: str


async def endpoint(body: LoginRequest):
    async with await asyncDbSession(XLNCDb) as session:
        result = await session.execute(
            select(XLNCDb.User).where(XLNCDb.User.username == body.username)
        )
        user = result.scalars().first()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        if not verify_password(body.password, user.password):
            raise HTTPException(status_code=400, detail="Wrong password")
        return {"status": "ok", "user_id": user.id}
