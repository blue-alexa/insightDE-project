import logging
import sys
sys.path.append("..")

from logging.config import dictConfig

from config import logging_config
from db.filing_index_dao import FilingIndexDAO
from tasks import download_parse_insert

dictConfig(logging_config)

# create logger
logger = logging.getLogger("BatchFilingManager.celery_main")

# retrieve url from database
logger.info(f"Starting retrieve urls from database")

filingIndex = FilingIndexDAO()
form_type = '13F-HR'
urls = filingIndex.get_url(form_type, start='2019-01-01')

task_queue = []
for url in urls:
    task_queue.append(download_parse_insert.delay(url, form_type))
logger.info(f"Added {len(urls)} tasks")

# python3 batch_filings.py