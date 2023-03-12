from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.db import get_db
from users import auth, users_models
from . import schemas, services


router = APIRouter()


@router.post('/remittance', response_model=schemas.RemittanceResponseSchema)
async def make_remittance(
        remittance_data: schemas.RemittanceRequestSchema,
        # TODO если успею заменю на нормальную авторизацию
        db: AsyncSession = Depends(get_db),
        user: users_models.User = Depends(auth.get_user)
) -> schemas.RemittanceResponseSchema:
    return await services.make_remittance(
        sender=user,
        recipient_name=remittance_data.recipient_name,
        amount=remittance_data.amount,
        db=db
    )