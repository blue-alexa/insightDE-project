import importlib
import os
import sys

import celery

from celery.utils.log import get_task_logger

from config import CELERY_BROKER_URL

app = celery.Celery('tasks',
                    broker=CELERY_BROKER_URL)

logger = get_task_logger(__name__)

sys.path.append(os.getcwd())

@app.task
def process_index(download_date):
    downloader = importlib.import_module('downloader')
    IndexParser = getattr(importlib.import_module('index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('dao'), 'FilingIndexDAO')

    index_file_content = downloader.download_index(download_date)
    if not index_file_content:
        return

    # Parse filing index doc
    ind_parser = IndexParser()
    records = ind_parser.parse(index_file_content, download_date)

    if not records:
        return

    # Insert filing index records to db
    filing_index_dao = FilingIndexDAO()
    filing_index_dao.bulk_insert(records)
    logger.info(f"Processed {len(records)} on {download_date.strftime('%Y-%m-%d')} index file")


# celery -A tasks worker --loglevel=info
