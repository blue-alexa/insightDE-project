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
    # check if form parser is available
    parser_name = f"FormParser_{form_type.replace('-', '_')}"
    parser_module = f'parsers.{parser_name}'
    try:
        FormParser = getattr(importlib.import_module(parser_module), parser_name)
    except ModuleNotFoundError:
        logger.error(f"Failed to loader form parser for {form_type}")
        return

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

# celery -A task worker --loglevel=info --logfile=celery_log.log

