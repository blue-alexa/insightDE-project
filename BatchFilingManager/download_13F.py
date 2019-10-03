import os, requests
from multiprocessing.pool import Pool

import logging
from logging.config import dictConfig

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
               'filename': 'es_feed_logger.log'},
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
logger = logging.getLogger("BatchFilingManager.download_13F")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

DB_USERNAME = 'edgar_user'
DB_PASSWORD = 'edgar_password'
DB_HOST = '34.219.152.31'
DB_PORT = '3306'
DB_NAME = 'edgar_db'

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

sql = "SELECT url FROM filing_index WHERE form_type = '13F-HR' AND date_filed >= '2019-01-01';"
rs = session.execute(sql).fetchall()

def generate_url():
    cnt = 0
    urls = []
    for row in rs:
        urls.append(row['url'])
        cnt += 1

        if cnt % 100 == 0:
            yield urls
            urls = []
    yield urls

target_folder = '/data2/filings/thirteenF_HR'

def download_filing(url):

    def fetch(url):
        web_session = requests.Session()
        try:
            response = web_session.get(url)

            if response.status_code == 200:
                content = response.content
                return content

        except Exception:
            pass

        return None

    content = fetch(url)
    if content:
        filename = url.split('/')[-1]
        filepath = os.path.join(target_folder, filename)
        with open(filepath, 'wb') as f:
            f.write(content)
            logger.info(f"Save to file {filepath}")

pool = Pool(processes=8)              # start 8 worker processes

for urls in generate_url():
    for i in pool.imap_unordered(download_filing, urls):
        print(i)
