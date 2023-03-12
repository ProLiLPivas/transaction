from pydantic import PositiveInt
from sqlalchemy import Update, update
from sqlalchemy.ext.asyncio import AsyncSession

from users import users_schemas, users_models
from . import exceptions


def gen_money_change_query(user_id: PositiveInt, money: float) -> Update:
    return update(users_models.User) \
        .values({users_models.User.money_amount: users_models.User.money_amount + money}) \
        .filter(users_models.User.id == user_id)


async def change_users_balance(
        amount: float, sender: users_schemas.UserSchema,
        recipient: users_schemas.UserSchema,
        db: AsyncSession
) -> None:
    try:
        await db.execute(gen_money_change_query(sender.id, -amount))
        await db.execute(gen_money_change_query(recipient.id, +amount))
        print(11)
    except:
        await db.rollback()
        raise exceptions.RemittanceException
    else:
        await db.commit()
