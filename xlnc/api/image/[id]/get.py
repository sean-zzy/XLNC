from fastapi import HTTPException, UploadFile
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from fastapi.responses import Response


async def endpoint(id: str):
    async with await asyncDbSession(XLNCDb) as session:
        try:
            result = await session.execute(
                select(XLNCDb.Item).where(XLNCDb.Item.id == id)
            )
            return Response(
                content=result.scalars().first().image, media_type="image/png"  # type: ignore
            )
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Item already exists")
