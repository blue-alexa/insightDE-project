import argparse
import os

from multiprocessing.pool import Pool
from time import time
import logging
from logging.config import dictConfig

from datetime import datetime, timedelta

from filing_download import filing_downloader

from config import logging_config


dictConfig(logging_config)

# create logger
logger = logging.getLogger("edgar_build.data_download_from_edgar")

parser = argparse.ArgumentParser()
parser.add_argument('start_date', help='Start downloading date, format YYYY-MM-DD')
parser.add_argument('end_date', help='Start downloading date, format YYYY-MM-DD')
parser.add_argument('target_folder', help='Target folder to store filing data')

val = parser.parse_args()
start_date = val.start_date
end_date = val.end_date
filing_path = val.target_folder

filing_start_date = datetime.strptime(start_date, '%Y-%m-%d')
filing_end_date = datetime.strptime(end_date, '%Y-%m-%d')

######### download filings ##############
logger.info(f"Start downloading daily filings")

pool = Pool(processes=8)              # start 8 worker processes

try:
    os.makedirs(filing_path, mode=0o777)
    logger.info(f"Successfully created directory {filing_path}")
except FileExistsError:
    pass

filing_params = []

d = filing_start_date
while d <= filing_end_date:
    if 0<= d.weekday() < 5:
        filename = f"master.{d.strftime('%Y%m%d')}.idx"
        if not os.path.exists(os.path.join(filing_path, filename)):
            filing_params.append((d, filing_path))
    d += timedelta(days=1)

filing_start = time()

for i in pool.imap_unordered(filing_downloader.download_filing, filing_params):
    print(i)

print(f"Elapsed Time: {time() - filing_start}")
