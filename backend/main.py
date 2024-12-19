from fastapi import FastAPI
from database import create_db_and_tables
from router import request_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    """Функция создания таблиц и данных в базе при первом запуске FastAPI"""
    await create_db_and_tables()


app.include_router(request_router, tags=["request"])
