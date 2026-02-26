# from app.core.db import DB
# db = DB()

def get_db():
    return db

def get_session():
    return db.get_session()