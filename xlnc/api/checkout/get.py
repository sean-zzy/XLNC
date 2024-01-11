from base64 import b64encode
from fastapi.responses import RedirectResponse
from httpx import AsyncClient
from uuid import uuid4
from fastapi import HTTPException, UploadFile
from pydantic import BaseModel
from pypox.database import asyncDbSession
from xlnc.database.SQLITE import XLNCDb
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

maya_checkout_public_key = "pk-Z0OSzLvIcOI2UIvDhdTGVVfRSSeiGStnceqwUE7n0Ah"
maya_checkout_secret_key = "sk-X8qolYjy62kIzEbr0QRK1h4b4KDVHaNcwMYk39jInSl"


async def endpoint(id: str, variant: str, user_id: str):
    maya_credentials = b64encode(
        f"{maya_checkout_public_key}:{maya_checkout_secret_key}".encode()
    ).decode("utf-8")

    async with await asyncDbSession(XLNCDb) as session:
        result = await session.execute(select(XLNCDb.Item).where(XLNCDb.Item.id == id))
        item = result.scalars().first()
        user = (
            await session.execute(select(XLNCDb.User).where(XLNCDb.User.id == user_id))
        ).scalar()
        if item is None:
            raise HTTPException(status_code=400, detail="Item not found")
        async with AsyncClient() as client:
            response = await client.post(
                f"https://pg-sandbox.paymaya.com/checkout/v1/checkouts/",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Basic {maya_credentials}",
                },
                json={
                    "totalAmount": {"value": item.price, "currency": "PHP"},
                    "buyer": {
                        "firstName": user.first_name,  # type: ignore
                        "middleName": "",
                        "lastName": user.last_name,  # type: ignore
                    },
                    "items": [
                        {
                            "name": item.name,
                            "description": "XLNC Product",
                            "quantity": 1,
                            "amount": {
                                "value": item.price,
                                "details": {
                                    "discount": "0",
                                    "serviceCharge": "0",
                                    "shippingFee": "0",
                                    "tax": "0",
                                    "subtotal": item.price,
                                },
                            },
                            "totalAmount": {
                                "value": item.price,
                                "details": {
                                    "discount": "0",
                                    "serviceCharge": "0",
                                    "shippingFee": "0",
                                    "tax": "0",
                                    "subtotal": item.price,
                                },
                            },
                        }
                    ],
                    "redirectUrl": {
                        "success": "http://localhost:8000",
                    },
                    "requestReferenceNumber": str(uuid4()),
                },
            )
            if response.status_code != 200:
                print(response.text)
                raise HTTPException(status_code=400, detail="Maya Error")
            else:
                return RedirectResponse(url=response.json()["redirectUrl"])
