from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, Index, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import QueuePool

from edgar_UI.config import DevConfig

engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0, poolclass=QueuePool)

def getconn():
    try:
        conn = engine.connect()
        Session = sessionmaker(bind=conn)
        session = Session()
        return session
    except Exception:
        pass

session = getconn()

Base = declarative_base()

class Index(Base):
    __tablename__ = 'filing_index'
    __table_args__ = (
        Index('date_index', 'date_filed'),
        Index('cik_form_index', 'cik', 'form_type'),
        Index('accession_no_index', 'accession_number')
    )

    id = Column(Integer, primary_key = True)
    cik = Column(String(20))
    company_name = Column(String(200))
    form_type = Column(String(30))
    date_filed = Column(Date)
    accession_number = Column(String(100))
    url = Column(String(200))
    date_created = Column(DateTime, default=datetime.utcnow)
    date_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Filing Index (cik={self.cik}, company_name={self.company_name}, form_type={self.form_type}, "\
            f"date_filed={self.date_filed.strftime('%Y-%m-%d')}>"
