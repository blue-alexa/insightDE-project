import importlib
import os
import sys

sys.path.append("..")

from datetime import datetime

import celery

from celery.utils.log import get_task_logger

from EdgarManagers.config import CELERY_BROKER_URL, local_timezone

app = celery.Celery('tasks',
                    broker=CELERY_BROKER_URL)

logger = get_task_logger(__name__)

@app.task
def process_index(download_date):
    """
    batch process index files
    """
    downloader = importlib.import_module('EdgarManagers.utils.downloader')
    IndexParser = getattr(importlib.import_module('EdgarManagers.parsers.index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('EdgarManagers.db.filing_index_dao'), 'FilingIndexDAO')

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


@app.task
def download_parse_insert(url, form_type):
    """
    batch process filing documents
    """
    # check if form parser is available
    parser_name = f"FormParser_{form_type.replace('-', '_')}"
    parser_module = f'EdgarManagers.parsers.{parser_name}'
    try:
        FormParser = getattr(importlib.import_module(parser_module), parser_name)
    except ModuleNotFoundError:
        logger.error(f"Failed to loader form parser for {form_type}")
        return

    # import downloader and esloader
    downloader = importlib.import_module('EdgarManagers.utils.downloader')
    ESLoader = getattr(importlib.import_module('EdgarManagers.elasticsearch.es_loader'), 'ESLoader')

    accession_no = url.split("/")[-1].split(".")[0]
    try:
        form_content = downloader.download(url)
        logger.info(f"Downloaded form {id}")
    except Exception:
        logger.error(f"Failed to download from {url}")
        return

    form_parser = FormParser()
    try:
        data = form_parser.parse(form_content, url)
        logger.info(f"Parsed form {url}")
    except Exception:
        logger.error(f"Failed to parse form {url}")
        return

    loader = ESLoader()
    index_name = form_type.lower()
    type_name = "form"
    try:
        loader.insert(index_name, type_name, accession_no, data)
        logger.info(f"Inserted form {accession_no} to elasticsearch")
    except Exception:
        logger.error(f"Failed to insert form {accession_no} to elasticsearch")


@app.task
def daily_job(download_date):
    """
    Daily download filing index and filing documents, write to MySQL and elastic search
    :return:
    """
    downloader = importlib.import_module('EdgarManagers.utils.downloader')
    IndexParser = getattr(importlib.import_module('EdgarManagers.parsers.index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('EdgarManagers.db.filing_index_dao'), 'FilingIndexDAO')
    HistoryDAO = getattr(importlib.import_module('EdgarManagers.db.history_dao'), 'HistoryDAO')
    ESLoader = getattr(importlib.import_module('EdgarManagers.elasticsearch.es_loader'), 'ESLoader')

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

        # check if form parser is available
        parser_name = f"FormParser_{form_type.replace('-', '_')}"
        parser_module = f'parsers.{parser_name}'
        try:
            FormParser = getattr(importlib.import_module(parser_module), parser_name)
        except ModuleNotFoundError:
            logger.error(f"Failed to loader form parser for {form_type}")
            return

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


# celery -A tasks worker --loglevel=info




