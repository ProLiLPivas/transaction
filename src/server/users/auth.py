from fastapi import HTTPException, status
from pydantic import PositiveInt

from common.db import SessionLocal
from users import managers, exceptions


async def get_user(user_id: PositiveInt):
    # TODO заменить на норм авторизацию
    async with SessionLocal() as db:
        try:
            return await managers.get_user_by_id(user_id=user_id, db=db)
        except exceptions.UserNotFoundException:
            return HTTPException(status.HTTP_401_UNAUTHORIZED)
