import logging
import sys

sys.path.append("..")

from datetime import datetime
from sqlalchemy import exc

from db_utils import get_db_conn
from config import local_timezone

history_logger = logging.getLogger("DailyJobs.dao.history")

class HistoryDAO(object):
    def __init__(self):
        self.conn = get_db_conn()

    def insert_history(self, download_date):
        """
        :param download_date: str YYYYMMDD
        :return:
        """
        today_str = local_timezone.localize(datetime.today()).strftime('%Y-%m-%d')
        download_date_str = datetime.strptime(download_date, "%Y%m%d").strftime('%Y-%m-%d')
        sql = f"INSERT INTO history(download_date, date_created, date_modified) VALUES('{download_date_str}'," \
                  f" '{today_str}', '{today_str}') ON DUPLICATE KEY UPDATE date_modified='{today_str}';"

        try:
            self.conn.execute(sql)
            self.conn.commit()
        except exc.SQLAlchemyError as e:
            history_logger.error(str(e))
        self.conn.close()

    def get_histroy(self, download_date):
        """
        :param download_date: str YYYYMMDD
        :return:
        """
        d = datetime.strptime(download_date, "%Y%m%d").strftime('%Y-%m-%d')
        sql = f"SELECT download_date, date_modified FROM history WHERE download_date='{d}';"
        rs = self.conn.execute(sql).fetchone()
        self.conn.close()
        if rs:
            return (rs['download_date'], rs['date_modified'])
        else:
            return None