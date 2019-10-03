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

@app.task
def daily_job():
    downloader = importlib.import_module('downloader')
    IndexParser = getattr(importlib.import_module('index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('dao'), 'FilingIndexDAO')
    HistoryDAO = getattr(importlib.import_module('dao'), 'HistoryDAO')
    ESLoader = getattr(importlib.import_module('es_loader'), 'ESLoader')

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
    filing_index_dao = FilingIndexDAO()
    filing_index_dao.bulk_insert(records)

    # Retrieve filing docs, parse, insert into ES
    for record in records:
        cik, company_name, form_type, date_filed, accession_no, url = record

        # Check if FormParser exists in the parsers folder
        parser_name = f"FormParser_{form_type.replace('-', '_')}"
        parser_path = os.path.join("../parsers", parser_name)
        if not os.path.exists(parser_path):
            continue
        parser_module = f'parsers.{parser_name}'
        FormParser = getattr(importlib.import_module(parser_module), parser_name)

        # Download form from SEC
        form_content = downloader.download(url)
        if not form_content:
            continue

        # Parse form with FormParser
        form_parser = FormParser()
        form_json = form_parser.parse(form_content, url)

        # Load json to ES
        loader = ESLoader()
        index_name = form_type.lower()
        type_name = "form"
        try:
            loader.insert(index_name, type_name, accession_no, form_json)
            logger.info(f"Inserted {form_type} form {accession_no} to elasticsearch")
        except Exception:
            logger.error(f"Failed to insert {form_type} form {accession_no} to elasticsearch")


    history_dao = HistoryDAO()
    history_dao.insert_history(download_date)







