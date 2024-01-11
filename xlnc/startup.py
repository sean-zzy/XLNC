from fastapi import FastAPI
from pypox import createAsyncEngine, getAsyncEngine
from xlnc.database.SQLITE import XLNCDb
from pypox.database import init_database_async

createAsyncEngine(XLNCDb, "aiosqlite", echo=True)


async def __call__(app: FastAPI):
    await init_database_async(getAsyncEngine(XLNCDb), XLNCDb)
