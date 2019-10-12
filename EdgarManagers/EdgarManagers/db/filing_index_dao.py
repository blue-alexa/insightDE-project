import logging

from sqlalchemy import exc

from .db_utils import get_db_conn

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

