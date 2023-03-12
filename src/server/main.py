from fastapi import FastAPI

from remittance import remittance_router
from users import users_router


app = FastAPI()


app.include_router(remittance_router)
app.include_router(users_router)

