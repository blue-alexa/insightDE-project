from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..config import SQLALCHEMY_DATABASE_URI

def get_db_conn():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session