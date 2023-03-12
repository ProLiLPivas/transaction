import decimal

from sqlalchemy.ext.asyncio import AsyncSession

from common.mq import RabbitQueue
from users import users_managers, users_schemas, users_exceptions
from . import exceptions, managers, schemas


async def make_remittance(
        amount: float,
        recipient_name: str,
        sender: users_schemas.UserSchema,
        db: AsyncSession
) -> schemas.RemittanceResponseSchema:
    try:
        recipient = await users_managers.get_user_by_name(username=recipient_name, db=db)
        check_user_balance(sender=sender, amount=amount)
        await managers.change_users_balance(
            amount=amount, sender=sender, recipient=recipient, db=db
        )

    except users_exceptions.UserNotFoundException as e:
        queues = [str(sender.id)]
        result = schemas.RemittanceResponseSchema(
            amount=amount, sender=sender.username, is_success=False, msg=str(e.detail)
        )
    except exceptions.RemittanceException as e:
        queues = [str(sender.id)]
        result = schemas.RemittanceResponseSchema(
            amount=amount, sender=sender.username, recipient=recipient.username, is_success=False, msg=str(e.detail)
        )
    else:
        queues = [str(recipient.id), str(sender.id)]
        result = schemas.RemittanceResponseSchema(
            amount=amount, sender=sender.username, recipient=recipient.username
        )
    finally:
        send_queue_message(queues=queues, message=result.form_mq_message())
        return result


def send_queue_message(queues: list[str], message: str):
    with RabbitQueue() as rmq:
        for queue in queues:
            rmq.send_message(queue_identifier=str(queue), message=message)


def check_user_balance(sender: users_schemas.UserSchema, amount: decimal):
    if amount > sender.money_amount:
        raise exceptions.RunOutOFMoneyException
