import sys
from datetime import datetime

from EdgarManagers.tasks import daily_job

# sys.path.append("..")

download_date = datetime(2019, 10, 9)
daily_job(download_date)