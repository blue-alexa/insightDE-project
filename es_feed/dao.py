import logging

from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import SQLALCHEMY_DATABASE_URI

def get_db_conn():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class FilingIndex(object):
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.logger = logging.getLogger("es_feed.dao")

    def get_url(self, form_type, start=None, end=None):
        if not start:
            start = '2000-01-01'
        if not end:
            end = datetime.today().strftime('%Y-%m-%d')
        sql = f"SELECT url FROM filing_index WHERE form_type = '{form_type}' AND date_filed >= '{start}' AND date_filed <= '{end}';"
        rs = self.db_conn.execute(sql).fetchall()
        urls = [row['url'] for row in rs]
        self.logger.info(f"Retrieved {len(urls)} urls, form: {form_type}, start: {start}, end: {end}")
        return urls

