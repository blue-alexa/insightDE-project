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

form_type = '13F-HR'
url = ""
download_parse_insert(url, form_type)