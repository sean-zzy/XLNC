from uuid import uuid4
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


class Comment(BaseModel):
    message: str
    rating: int
    user_id: str
    variant: str


async def endpoint(id: str, body: Comment):
    # add comment to product
    async with await asyncDbSession(XLNCDb) as session:
        user = (
            await session.execute(
                select(XLNCDb.User).where(XLNCDb.User.id == body.user_id)
            )
        ).scalar()
        session.add(XLNCDb.Comment(id=str(uuid4()), **body.model_dump(), name=user.username, item_id=id))  # type: ignore
        await session.commit()
        return {"status": "ok"}
