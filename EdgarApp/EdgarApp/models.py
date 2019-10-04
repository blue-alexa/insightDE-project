from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from EdgarApp.config import DevConfig

engine = create_engine(DevConfig.SQLALCHEMY_DATABASE_URI, pool_size=20, max_overflow=0, poolclass=QueuePool)

def getconn():
    try:
        conn = engine.connect()
        Session = sessionmaker(bind=conn)
        session = Session()
        return session
    except Exception:
        pass


class Index(object):
    def __init__(self):
        self.conn = getconn()

    def _sql_query_to_dict(self, sql):
        rs = self.conn.execute(sql).fetchall()
        data = [dict(row) for row in rs]
        return data

    def get_by_date_range(self, start_date, end_date):
        sql = f"SELECT * FROM filing_index WHERE date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
        data = self._sql_query_to_dict(sql)
        return data

    def get_by_cik_and_date_range(self, cik, start_date, end_date):
        sql = f"SELECT * FROM filing_index WHERE cik='{cik}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
        data = self._sql_query_to_dict(sql)
        return data

    def get_by_form_type_and_date_range(self, form_type, start_date, end_date):
        sql = f"SELECT * FROM filing_index WHERE form_type='{form_type}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
        data = self._sql_query_to_dict(sql)
        return data

    def get_by_cik_form_type_date_range(self, cik, form_type, start_date, end_date):
        sql = f"SELECT * FROM filing_index WHERE cik='{cik}'AND form_type='{form_type}'AND date_filed >= '{start_date}' AND date_filed <= '{end_date}';"
        data = self._sql_query_to_dict(sql)
        return data

