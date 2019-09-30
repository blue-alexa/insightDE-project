import logging
from logging.config import dictConfig

from config import logging_config
from dao import get_db_conn, FilingIndex
from task import download_parse_insert

dictConfig(logging_config)

# create logger
logger = logging.getLogger("es_feed.main")

# retrieve url from database
logger.info(f"Starting retrieve urls from database")
db_conn = get_db_conn()
filingIndex = FilingIndex(db_conn)
urls = filingIndex.get_url('13F-HR', start='2019-01-01')

print(urls[0])

# download filing from database
download_parse_insert(urls[0])

