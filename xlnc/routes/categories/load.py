from fastapi import Request
from sqlmodel import select
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb


async def load(request: Request):
    async with await asyncDbSession(XLNCDb) as session:
        item_data = {}

        items = await session.execute(select(XLNCDb.Item))
        for item in items.scalars().all():
            if item.category not in item_data:
                item_data[item.category] = []
            item_data[item.category].append(
                {
                    "item": item.name,
                    "price": item.price,
                    "rating": item.rating,
                    "id": item.id,
                }
            )
        print(item_data)
        return {
            "items": {
                **item_data,
            }
        }
