import sys
sys.path.append("..")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)

def get_db_conn():
    Session = sessionmaker(bind=engine)
    session = Session()
    return session