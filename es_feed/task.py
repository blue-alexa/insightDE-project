import importlib
import os
import sys

import celery

from celery.utils.log import get_task_logger

from config import CELERY_BROKER_URL

app = celery.Celery('task',
                    broker=CELERY_BROKER_URL)

logger = get_task_logger(__name__)
sys.path.append(os.getcwd())

@app.task
def download_parse_insert(url):
    downloader = importlib.import_module('downloader')
    ThirteenFHRParser = getattr(importlib.import_module('edgar_filing_parser'), 'ThirteenFHRParser')
    ESLoader = getattr(importlib.import_module('es_loader'), 'ESLoader')

    id = url.split("/")[-1].split(".")[0]
    try:
        content = downloader.download(url)
        logger.info(f"Downloaded form {id}")
    except Exception:
        logger.error(f"Failed to download from {url}")
        return

    content = content.decode('ISO-8859-1')
    parser = ThirteenFHRParser()
    try:
        data = parser.parse(content, id)
        logger.info(f"Parsed form {id}")
    except Exception:
        logger.error(f"Failed to parse form {id}")
        return

    loader = ESLoader()
    index_name = "13f-hr"
    type_name = "form"
    try:
        loader.insert(index_name, type_name, id, data)
        logger.info(f"Inserted form {id} to elasticsearch")
    except Exception:
        logger.error(f"Failed to insert form {id} to elasticsearch")

# celery -A task worker --loglevel=info --f celery_log.log


