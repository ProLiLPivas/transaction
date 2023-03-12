from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import get_db
from . import schemas, auth, users_models


router = APIRouter()


@router.get('/user', response_model=schemas.UserSchema)
async def make_remittance(
        user: users_models.User = Depends(auth.get_user)
) -> schemas.UserSchema:
    return schemas.UserSchema.from_orm(user)
