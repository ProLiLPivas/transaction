from abc import ABC

from fastapi import HTTPException
from starlette import status


class ExceptionWithSetParamsMixin(ABC):
    status_code: int
    detail: str

    def __init__(self, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class BaseEntityExceptionMixin(ExceptionWithSetParamsMixin, ABC):
    entity_name: str = ''
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = f'Unknown {entity_name} error'


class NotFoundEntityExceptionMixin(ExceptionWithSetParamsMixin, ABC):
    entity_name: str = ''
    status_code = status.HTTP_404_NOT_FOUND
    detail = f'Cant find {entity_name} error'




class ServerException(HTTPException): ...
