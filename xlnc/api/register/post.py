from uuid import uuid4
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


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str
    first_name: str
    last_name: str
    image: bytes = b""


async def endpoint(body: RegisterRequest):
    async with await asyncDbSession(XLNCDb) as session:
        try:
            body.password = get_password_hash(body.password)
            session.add(XLNCDb.User(id=str(uuid4()), **body.model_dump()))  # type: ignore
            await session.commit()
            return {"status": "ok"}
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="User already exists")
