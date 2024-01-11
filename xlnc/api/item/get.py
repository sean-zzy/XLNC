from fastapi import HTTPException, UploadFile
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


async def endpoint():
    async with await asyncDbSession(XLNCDb) as session:
        item_data = {}
        try:
            result = await session.execute(select(XLNCDb.Item))
            for item in result.scalars().all():
                if item.category not in item_data:
                    item_data[item.category] = []
                item_data[item.category].append(
                    {
                        "item": item.name,
                        "price": item.price,
                        "rating": item.rating,
                        "image": f"/api/image/{item.id}",
                    }
                )
            return item_data
        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Item already exists")
