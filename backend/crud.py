import uuid
from fastapi import HTTPException
from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from models import Request, User, Operator
from schemas import RequestStatus, OrderBy, TypeSort


async def get_request(uuid: str, db: AsyncSession):
    """Получить запись из таблицы request по uuid"""
    try:
        data = await db.execute(select(Request).where(Request.uuid == uuid))
        result = data.scalars().first()
        return result

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))


def generate_uuid():
    """Сгенерировать случайный uuid"""
    return str(uuid.uuid4())


# Здесь в идеале нужно из jwt токена получить id пользователя и передать в поле user_id
# Поскольку данный функционал не рассматривается, то для упрощения все обращения будет приходить от одного пользователя
async def add_data(data, db: AsyncSession):
    """Добавить данные об обращении"""
    request = Request(
        uuid=generate_uuid(),
        title=data.title,
        description=data.description,
        status=RequestStatus.INIT.value,
        user_id=1
    )
    try:
        db.add(request)
        await db.commit()
        return request
    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def assign_operator(uuid: str, operator_id: int, db: AsyncSession):
    """Назначить исполнителя на обращение"""
    try:
        result = await get_request(uuid=uuid, db=db)

        result.operator_id = operator_id
        result.status = RequestStatus.IN_PROGRESS.value

        await db.commit()
        return result

    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def close_user_request(uuid: str, db: AsyncSession):
    """Закрыть обращение"""
    try:
        data = await get_request(uuid=uuid, db=db)
        data.status = RequestStatus.CLOSED.value

        await db.commit()
        return data

    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def get_users_requests(db: AsyncSession, type_sort: str, status=str, order_by=str):
    """Получить полный список обращений"""
    try:
        query = select(Request)

        if status:
            query = query.where(Request.status == status)

        if order_by == OrderBy.DATE_CREATE:
            if type_sort == TypeSort.ASC:
                query = query.order_by(asc(Request.date_create))
            elif type_sort == TypeSort.DESC:
                query = query.order_by(desc(Request.date_create))

        data = await db.execute(query)
        result = data.scalars().all()
        return result

    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))
    finally:
        await db.close()


async def default_data(db: AsyncSession):
    user = User(username="Pavel Khramko", email="Pavel.Khramko@test.com")
    operator = Operator(name="Ivan Obramov")
    request = Request(
        uuid=generate_uuid(),
        title="Нет доступа к wiki",
        description="Под моей учетной записью нет доступа к Wiki, прошу добавить доступ",
        status="init",
        user_id=1
    )
    try:
        db.add(user)
        db.add(operator)
        db.add(request)
        await db.commit()
        await db.refresh(request)
        return request
    except Exception as error:
        await db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(error)}")
    finally:
        await db.close()
