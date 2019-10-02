import importlib
import os
import sys

from datetime import datetime

import celery

from celery.utils.log import get_task_logger

from config import CELERY_BROKER_URL

app = celery.Celery('task',
                    broker=CELERY_BROKER_URL)

logger = get_task_logger(__name__)

sys.path.append(os.getcwd())


def daily_job():
    downloader = importlib.import_module('downloader')
    IndexParser = getattr(importlib.import_module('index_parser'), 'IndexParser')
    FilingIndex = getattr(importlib.import_module('dao'), 'FilingIndex')
    FormParser = getattr(importlib.import_module('dao'), 'FormParser')
    History = getattr(importlib.import_module('dao'), 'History')

    # Retrieve filing index doc from SEC website
    download_date = datetime.today()
    index_file_content = downloader.download_index(download_date)
    if not index_file_content:
        return

    # Parse filing index doc
    ind_parser = IndexParser()
    records = ind_parser.parse(index_file_content, download_date)

    if not records:
        return

    # Insert filing index records to db
    filing_index = FilingIndex()
    filing_index.bulk_insert(records)

    # Retrieve filing docs, parse, insert into ES
    form_parser = FormParser()
    for record in records:
        cik, company_name, form_type, date_filed, accession_no, url = record
        code = form_parser.get_parser(form_type)
        if not code:
            continue
        exec(code)






