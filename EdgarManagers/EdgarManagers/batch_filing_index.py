import argparse
import logging
from logging.config import dictConfig
from datetime import datetime, timedelta

from config import logging_config
from tasks import process_index

dictConfig(logging_config)

# create logger
logger = logging.getLogger("EdgarManagers.batch_filing_index")

# retrieve url from database
logger.info(f"Starting retrieve urls from SEC database")

parser = argparse.ArgumentParser()
parser.add_argument('start_date', help='Start downloading date, format YYYY-MM-DD')
parser.add_argument('end_date', help='Start downloading date, format YYYY-MM-DD')

val = parser.parse_args()
start_date = val.start_date
end_date = val.end_date

logger.info(f"Retrieve filing index from {start_date} - {end_date}")

filing_start_date = datetime.strptime(start_date, '%Y-%m-%d')
filing_end_date = datetime.strptime(end_date, '%Y-%m-%d')

task_queue = []

d = filing_start_date
while d <= filing_end_date:
    if 0<= d.weekday() < 5:
        task_queue.append(process_index.delay(d))
    d += timedelta(days=1)
logger.info(f"Added {len(task_queue)} tasks")

# python3 batch_filing_index.py 2000-01-01 2000-02-01