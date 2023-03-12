from abc import ABC

from starlette import status

from common import exceptions


class BaseRemittanceException(exceptions.ServerException, ABC): ...


class RemittanceException(exceptions.BaseEntityExceptionMixin, BaseRemittanceException): ...


class RunOutOFMoneyException(RemittanceException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Run out of money'
