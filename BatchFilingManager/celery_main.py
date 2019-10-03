import logging
from logging.config import dictConfig

from config import logging_config
from dao import FilingIndexDAO
from task import download_parse_insert

dictConfig(logging_config)

# create logger
logger = logging.getLogger("BatchFilingManager.main")

# retrieve url from database
logger.info(f"Starting retrieve urls from database")

filingIndex = FilingIndexDAO()
form_type = '13F-HR'
urls = filingIndex.get_url(form_type, start='2019-01-01')

tasks = []
for url in urls:
    tasks.append(download_parse_insert.delay(url, form_type))