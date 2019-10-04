import logging
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from config import SQLALCHEMY_DATABASE_URI

def get_db_conn():
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class FilingIndexDAO(object):
    def __init__(self):
        self.conn = get_db_conn()
        self.logger = logging.getLogger("BatchIndexManager.dao.filing_index")

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