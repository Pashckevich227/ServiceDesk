from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from crud import add_data, assign_operator, close_user_request, get_users_requests
from schemas import RequestCreate, BaseRequest, AssignRequest, SendMessage, Request, OrderBy, TypeSort, RequestStatus

request_router = APIRouter()


@request_router.post('/create_request',
                     response_model=BaseRequest,
                     summary="Создать обращение")
async def create_request(
        data: RequestCreate,
        db: AsyncSession = Depends(get_async_session)
):
    result = await add_data(data=data, db=db)
    return BaseRequest(
        uuid=result.uuid,
        status=result.status,
        message="Обращение успешно создано"
    )


@request_router.patch(
    "/request/{uuid}/assign",
    response_model=BaseRequest,
    summary="Назначить исполнителя"
)
async def assign_request(
        uuid: str,
        assign: AssignRequest,
        db: AsyncSession = Depends(get_async_session)
):
    result = await assign_operator(uuid=uuid, operator_id=assign.operator_id, db=db)
    return BaseRequest(
        uuid=result.uuid,
        status=result.status,
        message="Назначен исполнитель на обращение"
    )


@request_router.post(
    "/request/{uuid}/message",
    response_model=BaseRequest,
    summary="Отправить сообщение пользователю"
)
async def send_message(uuid: str, message: SendMessage):
    return BaseRequest(
        uuid=uuid,
        status="in_progress",
        message=message.message
    )


@request_router.patch(
    "/request/{uuid}/close",
    response_model=BaseRequest,
    summary="Закрыть обращение"

)
async def close_request(uuid: str, db: AsyncSession = Depends(get_async_session)):
    result = await close_user_request(uuid=uuid, db=db)
    return BaseRequest(
        uuid=result.uuid,
        status=result.status,
        message="Обращение закрыто"
    )


@request_router.get(
    "/requests",
    response_model=list[Request],
    summary="Получить все обращения"
)
async def get_requests(
        status: Optional[RequestStatus] = RequestStatus.INIT,
        order_by: Optional[OrderBy] = OrderBy.DATE_CREATE,
        type_sort: Optional[TypeSort] = TypeSort.ASC,
        db: AsyncSession = Depends(get_async_session)
):
    data = await get_users_requests(db=db, status=status, order_by=order_by, type_sort=type_sort)
    return data
