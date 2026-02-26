from fastapi import FastAPI

#from app.core.db import DB
from app.routers import user, loan

#db = DB()
app = FastAPI()
# app.include_router(user.router)
# app.include_router(loan.router)

