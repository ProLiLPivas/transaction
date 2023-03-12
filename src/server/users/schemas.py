from pydantic import BaseModel, PositiveInt


class UserSchema(BaseModel):
    id: PositiveInt
    username: str
    money_amount: float

    class Config:
        orm_mode = True