import os, requests

from multiprocessing.pool import Pool
import logging
from logging.config import dictConfig

source = 'download_list.csv'
# target_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filings')
target_folder = '/data2/filings'

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
logger = logging.getLogger("index_to_db.download_filings")


def download_filing(url):

    def fetch(url):
        web_session = requests.Session()
        try:
            response = web_session.get(url)

            if response.status_code == 200:
                content = response.content
                logger.info(f"Downloaded from link {url}")
                return content

        except Exception:
            logger.error(f"Failed to download from link {url}")

        return None

    filename = url.split("/")[-1]
    filepath = os.path.join(target_folder, filename)

    content = fetch(url)
    if content:
        with open(filepath, 'wb') as f:
            f.write(content)
            logger.info(f"Save to file {filepath}")

def generate_urls():
    cnt = 0
    urls = []
    with open(source, 'r') as f:
        for line in f:
            accession_no, url = line.strip().split('|')
            urls.append(url)
            cnt += 1

            if cnt % 100 == 0:
                yield urls
                urls = []

    yield urls


pool = Pool(processes=8)              # start 8 worker processes

for urls in generate_urls():
    for i in pool.imap_unordered(download_filing, urls):
        print(i)
