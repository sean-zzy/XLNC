import random
from fastapi import HTTPException, Request, UploadFile
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError


async def load(request: Request):
    async with await asyncDbSession(XLNCDb) as session:
        item_data = {}
        try:
            result: XLNCDb.Item = (  # type: ignore
                await session.execute(
                    select(XLNCDb.Item).where(
                        XLNCDb.Item.id == request.query_params.get("id")
                    )
                )
            ).scalar()

            random_items = (
                (
                    await session.execute(
                        select(XLNCDb.Item).where(
                            XLNCDb.Item.category == result.category
                        )
                    )
                )
                .scalars()
                .all()
            )

            comments = (await session.execute(select(XLNCDb.Comment))).scalars().all()

            print("comments", comments)

            return {
                "head": {
                    "title": "XLNC " + result.name,
                },
                "item": result.name,
                "price": result.price,
                "rating": result.rating,
                "image": f"/api/image/{result.id}",
                "id": result.id,
                "recommendations": [
                    {
                        "item": x.name,
                        "price": x.price,
                        "rating": x.rating,
                        "image": f"/api/image/{x.id}",
                        "id": x.id,
                    }
                    for x in random_items
                ],
                "comments": [
                    {
                        "user": x.name,
                        "comment": x.message,
                        "rating": x.rating,
                        "date": x.date,
                        "variant": x.variant,
                    }
                    for x in comments
                    if x.item_id == result.id
                ],
                "description": "",
            }

        except IntegrityError as e:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Item already exists")
