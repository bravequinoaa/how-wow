from app.core.config import Config

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.models import Base


class DB():
    def __init__(self):
        self.engine = None
        self.session = None
        self.init_db()
        self.init_models()
        self.init_session()

    def init_db(self):
        engine_path = Config['database']['engine_path']
        print(engine_path)

        self.engine = create_engine(engine_path, echo=True)
    
    def init_models(self):
        Base.metadata.create_all(self.engine)

    def init_session(self):
        self.session = Session(self.engine)     

    def get_session(self):
        return self.session