from abc import ABC

from common import exceptions


class BaseUserException(exceptions.ServerException, ABC):
    entity_name = 'user'


class UserException(exceptions.BaseEntityExceptionMixin, BaseUserException): ...


class UserNotFoundException(exceptions.NotFoundEntityExceptionMixin, BaseUserException):
    detail = 'Cant find user'
