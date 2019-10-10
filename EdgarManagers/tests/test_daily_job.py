from datetime import datetime

from ..tasks import daily_job

download_date = datetime(2019, 10, 9)
daily_job(download_date)