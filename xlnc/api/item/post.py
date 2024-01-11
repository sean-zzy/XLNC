from uuid import uuid4
from fastapi import HTTPException, UploadFile
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


async def endpoint(
    category: str,
    name: str,
    colors: str,
    rating: int,
    sizes: str,
    price: float,
    image: UploadFile,
):
    async with await asyncDbSession(XLNCDb) as session:
        item = XLNCDb.Item(  # type: ignore
            id=str(uuid4()),
            category=category,
            name=name,
            colors=colors,
            rating=rating,
            sizes=sizes,
            image=await image.read(),
            price=price,
        )
        session.add(item)
        await image.close()
        await session.commit()
        return {
            "status": "ok",
        }
