import datetime

from pydantic import BaseModel, validator


class RemittanceRequestSchema(BaseModel):
    amount: float
    recipient_name: str

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise TypeError('Value must be grater then zero')
        if len(str(v).split('.')[-1]) > 2:
            raise TypeError()
        return v


class RemittanceResponseSchema(BaseModel):
    msg: str = ''
    is_success: bool = True
    amount: float
    sender: str
    recipient: str = ''

    def form_mq_message(self) -> str:
        return f'[{datetime.datetime.now()}] ' \
            f'Remittance: {self.sender} ' \
            f'-> {self.recipient} ' \
            f'({self.amount} $) ' \
            f'{"SUCCEED" if self.is_success else "FAILED"} ' \
            f'{self.msg}'
