import os

from multiprocessing.pool import Pool
from time import time
import logging
from logging.config import dictConfig

from datetime import date, timedelta

from filing_download import filing_downloader
from log_download import log_downloader
from log_download import log_preprocess

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
        },
    handlers = {
        'fh': {'class': 'logging.FileHandler',
               'formatter': 'f',
               'level': logging.INFO,
               'filename': 'logger.log'},
        'ch': {'class': 'logging.StreamHandler',
               'formatter': 'f',
               'level': logging.INFO}
        },
    root = {
        'handlers': ['fh', 'ch'],
            'level': logging.INFO,
        }
)

dictConfig(logging_config)

# create logger
logger = logging.getLogger("edgar_build.main")

######### download filings ##############
logger.info(f"Start downloading daily filings")

pool = Pool(processes=8)              # start 8 worker processes

filing_path = 'data/filings'
try:
    os.makedirs(filing_path, mode=0o777)
    logger.info(f"Successfully created directory {filing_path}")
except FileExistsError:
    pass

filing_params = []
filing_start_date = date(2019, 8, 17)

filing_end_date = date(2019, 9, 16)

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

############### Download log ####################
logger.info(f"Start downloading log files")

pool = Pool(processes=8)              # start 8 worker processes

log_raw_data_path = 'raw_data/log_file'

try:
    os.makedirs(log_raw_data_path, mode=0o777)
    logger.info(f"Successfully created directory {log_raw_data_path}")
except FileExistsError:
    pass

log_params = []
log_start_date = date(2017, 1, 1)
log_end_date = date(2017, 1, 2)
d = log_start_date
while d <= log_end_date:
    filename = f"log{d.strftime('%Y%m%d')}.zip"
    if not os.path.exists(os.path.join(log_raw_data_path, filename)):
        log_params.append((d, log_raw_data_path))
    d += timedelta(days=1)

log_start = time()

for i in pool.imap_unordered(log_downloader.download_log, log_params):
    print(i)

print(f"Elapsed Time: {time() - log_start}")

############ unzip log files and save csv format only ##############
target_log_path = 'data/log_file'
try:
    os.makedirs(target_log_path, mode=0o777)
    logger.info(f"Successfully created directory {target_log_path}")
except FileExistsError:
    pass

log_preprocess.unzip_and_save_csv(log_raw_data_path, target_log_path)

################### upload to S3 #########################

import boto3
import glob

filing_path = 'data/filings'
log_path = 'data/log_file'
bucket_name = 'miniminds-edgar-data'

s3 = boto3.resource('s3')

for f in glob.glob(filing_path + '/*.idx'):
    data = open(f, 'rb')
    s3.Bucket(bucket_name).put_object(Key=filing_path, Body=data)
    logger.info("Successfuly uploaded Filing {f} to S3")

for f in glob.glob(log_path + '/*.csv'):
    data = open(f, 'rb')
    s3.Bucket(bucket_name).put_object(Key=log_path, Body=data)
    logger.info("Successfuly uploaded Log {f} to S3")