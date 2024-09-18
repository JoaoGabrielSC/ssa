from models.base import Base
from models.region import Region

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

class Database:
    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url)
        self.create_tables()
    
    def get_engine(self):
        return self.engine
    
    def new_session(self):
        Session = sessionmaker(bind=self.get_engine())
        session = Session()
        return session
    
    def create_tables(self):
        Base.metadata.create_all(self.get_engine())
