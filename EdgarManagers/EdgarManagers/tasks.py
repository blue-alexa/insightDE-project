import importlib
import sys
import time
import celery

sys.path.append(".")

from celery.utils.log import get_task_logger

from config import CELERY_BROKER_URL
from utils.funcs import time_profile

app = celery.Celery('tasks',
                    broker=CELERY_BROKER_URL)

logger = get_task_logger(__name__)

@app.task
@time_profile(logger)
def process_index(download_date):
    """
    batch process index files
    :param download_date: str YYYYMMDD
    :return:
    """
    logger.info(f"Start processing filing index {download_date}")
    downloader = importlib.import_module('utils.downloader')
    IndexParser = getattr(importlib.import_module('edgar_parsers.index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('db.filing_index_dao'), 'FilingIndexDAO')

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
    logger.info(f"Number of records processed {len(records)} in {download_date} index file")

@app.task
@time_profile(logger)
def download_parse_insert(url, form_type):
    """
    batch process filing documents
    """
    # check if form parser is available
    parser_name = f"FormParser_{form_type.replace('-', '_')}"
    parser_module = f'edgar_parsers.{parser_name}'
    try:
        FormParser = getattr(importlib.import_module(parser_module), parser_name)
    except ModuleNotFoundError:
        logger.error(f"Failed to loader form parser for {form_type}")
        return

    # import downloader and esloader
    downloader = importlib.import_module('utils.downloader')
    ESLoader = getattr(importlib.import_module('elasticsearch_dao.es_loader'), 'ESLoader')

    download_start = time.time()
    accession_no = url.split("/")[-1].split(".")[0]
    try:
        form_content = downloader.download(url)
        logger.info(f"Downloaded form {id} finished in {time.time()-download_start} seconds")
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

    parser_start = time.time()
    loader = ESLoader()
    index_name = form_type.lower()
    type_name = "form"
    try:
        loader.insert(index_name, type_name, accession_no, data)
        logger.info(f"Inserted form {accession_no} to elasticsearch finished in {time.time()-parser_start} seconds")
    except Exception:
        logger.error(f"Failed to insert form {accession_no} to elasticsearch")


@app.task
@time_profile(logger)
def daily_job(download_date):
    """
    Daily download filing index and filing documents, write to MySQL and elastic search
    :param download_date: str YYYYMMDD
    :return:
    """
    downloader = importlib.import_module('utils.downloader')
    IndexParser = getattr(importlib.import_module('edgar_parsers.index_parser'), 'IndexParser')
    FilingIndexDAO = getattr(importlib.import_module('db.filing_index_dao'), 'FilingIndexDAO')
    HistoryDAO = getattr(importlib.import_module('db.history_dao'), 'HistoryDAO')
    ESLoader = getattr(importlib.import_module('elasticsearch_dao.es_loader'), 'ESLoader')

    download_index_start = time.time()
    index_file_content = downloader.download_index(download_date)
    if not index_file_content:
        return

    logger.info(f"Finish download index file in {time.time()-download_index_start} seconds")

    parse_index_start = time.time()
    # Parse filing index doc
    ind_parser = IndexParser()
    records = ind_parser.parse(index_file_content, download_date)

    if not records:
        return

    logger.info(f"Finished parsing index file in {time.time()-parse_index_start} seconds")

    index_insert_start = time.time()
    # Insert filing index records to db
    filing_index_dao = FilingIndexDAO()
    filing_index_dao.bulk_insert(records)
    logger.info(f"Finished inserting index records to db in {time.time()-index_insert_start} seconds")

    # Retrieve filing docs, parse, insert into ES
    for record in records:
        cik, company_name, form_type, date_filed, accession_no, url = record

        # check if form parser is available
        parser_name = f"FormParser_{form_type.replace('-', '_')}"
        parser_module = f'edgar_parsers.{parser_name}'
        try:
            FormParser = getattr(importlib.import_module(parser_module), parser_name)
        except ModuleNotFoundError:
            logger.error(f"Failed to loader form parser for {form_type}")
            continue

        download_filing_start = time.time()
        # Download form from SEC
        form_content = downloader.download(url)
        if not form_content:
            continue
        logger.info(f"Finished downloading filing in {time.time()-download_filing_start} seconds")

        parse_filing_start = time.time()
        # Parse form with FormParser
        form_parser = FormParser()
        form_json = form_parser.parse(form_content, url)
        logger.info(f"Finished parsing filing in {time.time()-parse_filing_start} seconds")

        insert_es_start = time.time()
        # Load json to ES
        loader = ESLoader()
        index_name = form_type.lower()
        type_name = "form"
        try:
            loader.insert(index_name, type_name, accession_no, form_json)
            logger.info(f"Inserted {form_type} form {accession_no} to elasticsearch")
            logger.info(f"Finished insert filing to elastic search in {time.time() - insert_es_start} seconds")
        except Exception:
            logger.error(f"Failed to insert {form_type} form {accession_no} to elasticsearch")

    history_dao = HistoryDAO()
    history_dao.insert_history(download_date)


# celery -A tasks worker --loglevel=info
# celery -A tasks worker -f celery_worker_log_filings.log --loglevel=info




