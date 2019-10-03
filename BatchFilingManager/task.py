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
def download_parse_insert(url, form_type):
    batch_manager = importlib.import_module("BatchFilingManager")
    logger.info(f"{batch_manager.__dict__}")
    # check if form parser is available
    parser_name = f"FormParser_{form_type.replace('-', '_')}"
    parser_path = os.path.join(os.getcwd(), "parsers", parser_name)
    logger.info(f"parser_name is {parser_name}")
    logger.info(f"parser_path is {parser_path}")
    if not os.path.exists(parser_path):
        logger.error(f"Failed to loader form parser for {form_type}")
        return
    parser_module = f'parsers.{parser_name}'
    logger.info(f"parser_module is {parser_module}")
    FormParser = getattr(importlib.import_module(parser_module), parser_name)
    logger.info(f"Access {FormParser.doc_pattern}")
    """
    # import downloader and esloader
    downloader = importlib.import_module('downloader')
    ESLoader = getattr(importlib.import_module('es_loader'), 'ESLoader')

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
    """
# celery -A task worker --loglevel=info --logfile=celery_log.log

