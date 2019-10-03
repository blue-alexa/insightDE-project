import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from config import SQLALCHEMY_DATABASE_URI, local_timezone

def get_db_conn():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class FilingIndexDAO(object):
    def __init__(self):
        self.conn = get_db_conn()
        self.logger = logging.getLogger("DailyJobs.dao.filing_index")

    def bulk_insert(self, records):
        for record in records:
            cik, company_name, form_type, date_filed, accession_no, url = record
            sql = f"INSERT INTO filing_index (cik, company_name, form_type, date_filed, accession_number, url) " \
                f"VALUES('{cik}','{company_name}','{form_type}','{date_filed.strftime('%Y-%m-%d')}','{accession_no}','{url}');"
            try:
                self.conn.execute(sql)
                self.conn.commit()
            except exc.SQLAlchemyError:
                self.logger.error(f"Failed to insert line: {record}")

class HistoryDAO(object):
    def __init__(self):
        self.conn = get_db_conn()
        self.logger = logging.getLogger("DailyJobs.dao.history")

    def insert_history(self, download_date):
        today_str = local_timezone.localize(datetime.today()).strftime('%Y-%m-%d')
        download_date_str = download_date.strftime('%Y-%m-%d')
        sql = f"INSERT INTO history(download_date, date_created, date_modified) VALUES('{download_date_str}'," \
                  f" '{today_str}', '{today_str}') ON DUPLICATE KEY UPDATE date_modified='{today_str}';"
        self.conn.execute(sql)
        self.conn.commit()

    def get_histroy(self, download_date):
        sql = f"SELECT download_date, date_modified FROM history WHERE download_date='{download_date.strftime('%Y-%m-%d')}';"
        rs = self.conn.execute(sql).fetchone()
        if rs:
            return (rs['download_date'], rs['date_modified'])
        else:
            return None

