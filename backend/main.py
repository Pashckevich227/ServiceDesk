from fastapi import FastAPI
from database import create_db_and_tables, async_session_maker
from router import request_router
from crud import default_data

app = FastAPI(title="ServiceDesk")


@app.on_event("startup")
async def startup():
    """Функция создания таблиц и данных в базе при первом запуске FastAPI"""
    await create_db_and_tables()
    async with async_session_maker() as session:
        await default_data(session)


app.include_router(request_router, tags=["request"])
