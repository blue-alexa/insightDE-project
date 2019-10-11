import logging
from logging.config import dictConfig

from EdgarManagers.config import logging_config
from EdgarManagers.db.filing_index_dao import FilingIndexDAO
from EdgarManagers.tasks import download_parse_insert

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