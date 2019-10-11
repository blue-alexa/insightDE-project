import logging
from datetime import datetime

from EdgarManagers.db.db_utils import get_db_conn
from EdgarManagers.config import local_timezone

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