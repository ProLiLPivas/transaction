from pydantic import PositiveInt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models, exceptions


async def get_user_or_none(conditional, db: AsyncSession) -> models.User | None:
    result = await db.scalars(select(models.User).filter(conditional))
    return result.one_or_none()


async def get_user_by_id(user_id: PositiveInt, db: AsyncSession) -> schemas.UserSchema:
    if user := await get_user_or_none((models.User.id == user_id), db=db):
        return schemas.UserSchema.from_orm(user)
    raise exceptions.UserNotFoundException


async def get_user_by_name(username: str, db: AsyncSession) -> schemas.UserSchema:
    if user := await get_user_or_none((models.User.username == username), db=db):
        return schemas.UserSchema.from_orm(user)
    raise exceptions.UserNotFoundException

