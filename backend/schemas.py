from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime


class RequestStatus(str, Enum):
    """Статусы заказов"""
    INIT = 'init'
    IN_PROGRESS = 'in_progress'
    CLOSED = 'closed'


class OrderBy(str, Enum):
    """Варианты полей сортировки"""
    DATE_CREATE = 'date_create'


class TypeSort(str, Enum):
    """Тип сортировки"""
    ASC = "asc"
    DESC = "desc"


class RequestCreate(BaseModel):
    """Поля создания обращения"""
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


class Request(BaseModel):
    """Поля обращения"""
    uuid: str
    title: str
    description: str
    status: RequestStatus
    date_create: datetime
    user_id: int
    operator_id: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True


class BaseRequest(BaseModel):
    """Ответ на запрос"""
    uuid: str
    status: str
    message: str


class AssignRequest(BaseModel):
    """Назначение оператора на заявку"""
    operator_id: int


class SendMessage(BaseModel):
    """Формат сообщения пользователю"""
    message: str