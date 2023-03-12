from sqlalchemy import Column, Integer, String, DECIMAL

from common.db import Base


class User(Base):
    __table_args__ = {'schema': 'test'}
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    money_amount = Column(DECIMAL, nullable=False, default=0.0, server_default='0.0')
