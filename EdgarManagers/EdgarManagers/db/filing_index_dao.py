import logging
import sys

sys.path.append("..")

from sqlalchemy import exc

from .db_utils import get_db_conn

filing_index_logger = logging.getLogger("DailyJobs.dao.filing_index")

class FilingIndexDAO(object):
    def __init__(self):
        self.conn = get_db_conn()

    def bulk_insert(self, records):
        for record in records:
            cik, company_name, form_type, date_filed, accession_no, url = record
            sql = f"INSERT INTO filing_index (cik, company_name, form_type, date_filed, accession_number, url) " \
                f"VALUES('{cik}','{company_name}','{form_type}','{date_filed}','{accession_no}','{url}');"
            try:
                self.conn.execute(sql)
                self.conn.commit()
            except exc.SQLAlchemyError as e:
                filing_index_logger.error(str(e))

        self.conn.close()

    def check_record_no_by_date(self, date_filed):
        """
        return number of records on specific file date
        :param date_filed: str YYYY-MM-DD
        :return: int
        """
        sql = f"SELECT COUNT(id) AS counts FROM filing_index WHERE date_filed='{date_filed}';"
        try:
            rs = self.conn.execute(sql).fetchone()
            return (rs['counts'])
        except exc.SQLAlchemyError as e:
            filing_index_logger.error(str(e))

        self.conn.close()

    def get_url(self, form_type, start=None):
        sql = f"SELECT url FROM filing_index WHERE form_type='{form_type}' and date_filed>='{start}';"
        try:
            rs = self.conn.execute(sql).fetchall()
            return ([row['url'] for row in rs])
        except exc.SQLAlchemyError as e:
            filing_index_logger.error(str(e))

        self.conn.close()


